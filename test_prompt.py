"""Test custom_rewrite prompt quality and shutdown flow"""
import sys, asyncio
sys.path.insert(0, '.')

from omnitype.storage.config import get_config_manager
from omnitype.ai.provider_factory import get_provider_factory, PromptBuilder

cfg = get_config_manager().get()

test_cases = [
    ("hello", "translate to telugu"),
    ("how r u , narasimha", "translate to telugu"),
    ("i am fine", "make it formal"),
    ("this is bad", "make it positive and friendly"),
]

async def run():
    provider = get_provider_factory().get_provider(cfg)
    for text, instruction in test_cases:
        sys_p = PromptBuilder.build_system_prompt("custom_rewrite", instruction)
        usr_p = PromptBuilder.build_user_prompt(text, "custom_rewrite", instruction)
        print(f"\nInput: {repr(text)}")
        print(f"Task:  {repr(instruction)}")
        print(f"User prompt:\n  {repr(usr_p)}")
        try:
            resp = await asyncio.wait_for(provider.complete(usr_p, system=sys_p), timeout=15)
            result = resp.text.strip()
            print(f"Result ({len(result)} chars): {repr(result[:200])}")
            # Check for signs of verbosity
            bad_phrases = ["here is", "certainly", "sure!", "of course", "the translation", "the result"]
            if any(p in result.lower() for p in bad_phrases):
                print("  ⚠ WARNING: model added preamble!")
            else:
                print("  ✅ Clean output")
        except Exception as e:
            print(f"  ERROR: {e}")

asyncio.run(run())
