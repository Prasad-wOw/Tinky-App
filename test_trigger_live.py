"""
Auto-typing trigger pipeline test — types 'hello .g' itself after 2s delay.
Tests the full pipeline: hook → parser → signal → async → AI → replace.
"""
import sys, asyncio, threading, time
sys.path.insert(0, ".")
print("=== OmniType Auto-Trigger Pipeline Test ===\n", flush=True)

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal
app = QApplication.instance() or QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
import qasync
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)

from omnitype.storage.config import get_config_manager
cm = get_config_manager()
cfg = cm.get()
cfg.enabled = True
print(f"Config: provider={cfg.ai_provider}, key_set={bool(cfg.api_key_encrypted)}", flush=True)

from omnitype.core.trigger_parser import TriggerParser, TriggerMatch
parser = TriggerParser(cfg)

results = {"hook_fired": False, "signal_received": False, "ai_ok": False, "replace_ok": False}

class Bridge(QObject):
    sig = Signal(object)
    def __init__(self):
        super().__init__()
        self.sig.connect(self.on_trigger)
    def on_trigger(self, match):
        results["signal_received"] = True
        print(f"[3] Qt signal received on main thread: type={match.trigger_type}, orig='{match.original_text}'", flush=True)
        asyncio.ensure_future(self.process(match))
    async def process(self, match):
        print(f"[4] Async pipeline running...", flush=True)
        from omnitype.ai.provider_factory import get_provider_factory
        try:
            provider = get_provider_factory().get_provider(cfg)
            resp = await asyncio.wait_for(
                provider.complete(f"Correct the grammar of: {match.original_text}"),
                timeout=20
            )
            results["ai_ok"] = True
            ai_text = resp.text.strip()
            print(f"[5] AI responded: '{ai_text[:80]}'", flush=True)
            from omnitype.core.replacer import TextReplacer
            replacer = TextReplacer(cfg)
            ok = await replacer.replace(match, ai_text)
            results["replace_ok"] = ok
            print(f"[6] Replacement: {'OK' if ok else 'FAILED'}", flush=True)
        except Exception as e:
            print(f"[ERROR in pipeline] {type(e).__name__}: {e}", flush=True)
        finally:
            app.quit()

bridge = Bridge()

from omnitype.core.keyboard_listener import KeyboardListener
listener = KeyboardListener(
    trigger_parser=parser,
    on_trigger=lambda m: (results.__setitem__("hook_fired", True),
                          print(f"[2] Hook fired: type={m.trigger_type} orig='{m.original_text}'", flush=True),
                          bridge.sig.emit(m)),
    config=cfg
)
listener.start()
print("[1] KeyboardListener started. Auto-typing 'hello .g' in 2s...\n", flush=True)

def auto_type():
    time.sleep(2)
    import keyboard as kb
    kb.write("hello ", delay=0.05)
    kb.write(".g", delay=0.05)
    print("    [AUTO] Typed 'hello .g'", flush=True)

threading.Thread(target=auto_type, daemon=True).start()

async def main():
    await asyncio.sleep(30)  # timeout

with loop:
    loop.run_until_complete(main())

listener.stop()
print("\n=== RESULTS ===", flush=True)
for k, v in results.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}", flush=True)
