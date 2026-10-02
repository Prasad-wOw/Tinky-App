"""Diagnose both issues: backspace count and custom rewrite"""
import sys, asyncio, re
sys.path.insert(0, '.')

# --- Issue 2: Test triple-dot regex ---
print("=== Issue 2: Triple-dot regex test ===")
from omnitype.storage.config import get_config_manager
from omnitype.core.trigger_parser import TriggerParser, _TRIPLE_DOT_RE

cfg = get_config_manager().get()
parser = TriggerParser(cfg)

tests = [
    "how r u , narasimha ... translate to telugu...",
    "hello world ... make it formal...",
    "fix this ... shorter...",
]
for t in tests:
    m = _TRIPLE_DOT_RE.match(t)
    pm = parser.parse(t)
    print(f"  Input: {repr(t)}")
    print(f"  Regex: {'MATCH' if m else 'NO MATCH'}", end="")
    if m:
        print(f" orig={repr(m.group(1).strip())} instr={repr(m.group(2).strip())}", end="")
    print()
    print(f"  Parser: {pm.trigger_type if pm else 'None'}, orig={repr(pm.original_text) if pm else 'N/A'}")
    print()

# --- Issue 1: Test total_chars vs actual characters ---
print("=== Issue 1: Backspace count test ===")
# Simulate keyboard buffer accumulation with space fix
def simulate_buffer(text):
    """Simulate what the keyboard listener builds in the buffer"""
    buf = []
    for ch in text:
        if ch == '\n':
            buf.clear()  # Enter clears buffer
        else:
            buf.append(ch)
    return ''.join(buf)

test_cases = [
    "Hello world .g",          # simple
    "Hello world\nFix this .g", # Enter clears buffer, only "Fix this .g" in buffer
    "Fix grammar .professional",
    "how r u ... translate to telugu...",
]
for case in test_cases:
    buf = simulate_buffer(case)
    m = parser.parse(buf)
    if m:
        print(f"  Input: {repr(case)}")
        print(f"  Buffer: {repr(buf)} ({len(buf)} chars)")
        print(f"  orig_text: {repr(m.original_text)} ({len(m.original_text)} chars)")
        print(f"  total_chars (backspaces to send): {m.total_chars}")
        # What's actually visible at cursor in Notepad?
        # = whatever the user typed since last newline
        typed_on_line = buf  # after Enter clears buffer
        print(f"  Expected to delete: {repr(typed_on_line)} ({len(typed_on_line)} chars)")
        match = "OK" if m.total_chars == len(typed_on_line) else f"MISMATCH (sends {m.total_chars} but {len(typed_on_line)} on line)"
        print(f"  Status: {match}")
    print()

# --- Issue 2 deeper: Test prompt builder ---
print("=== Issue 2: PromptBuilder output ===")
from omnitype.ai.provider_factory import PromptBuilder
sys_p = PromptBuilder.build_system_prompt("custom_rewrite", "translate to telugu")
usr_p = PromptBuilder.build_user_prompt("how r u , narasimha", "custom_rewrite", "translate to telugu")
print(f"  System: {repr(sys_p)}")
print(f"  User:   {repr(usr_p)}")
print()

# --- Issue 2 even deeper: actually call Gemini ---
print("=== Issue 2: Live Gemini custom_rewrite call ===")
async def test_ai():
    from omnitype.ai.provider_factory import get_provider_factory
    try:
        provider = get_provider_factory().get_provider(cfg)
        resp = await asyncio.wait_for(
            provider.complete(usr_p, system=sys_p),
            timeout=15
        )
        print(f"  Response: {repr(resp.text[:200])}")
        print(f"  Empty? {not resp.text.strip()}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")

asyncio.run(test_ai())
