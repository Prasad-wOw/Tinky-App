"""
OmniType startup diagnostic — identifies the exact step that crashes.
Run: python diagnose.py
"""
import sys
import asyncio
import traceback

sys.path.insert(0, ".")

print("=== OmniType Startup Diagnostic ===", flush=True)

# Step 1: Qt
print("Step 1: Creating QApplication...", flush=True)
from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
print("  QApplication OK", flush=True)

# Step 2: qasync
print("Step 2: Creating qasync event loop...", flush=True)
import qasync
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)
print("  qasync loop OK", flush=True)


async def diagnose():
    print("Step 3: setup_logging...", flush=True)
    from omnitype.utils.logger import setup_logging
    setup_logging()
    print("  logging OK", flush=True)

    print("Step 4: ConfigManager...", flush=True)
    from omnitype.storage.config import get_config_manager
    cm = get_config_manager()
    cfg = cm.get()
    print(f"  config OK (provider={cfg.ai_provider}, key_set={bool(cfg.api_key_encrypted)})", flush=True)

    print("Step 5: DatabaseManager...", flush=True)
    from omnitype.storage.database import get_database
    db = get_database()
    await db.initialize()
    print("  database OK", flush=True)

    print("Step 6: HistoryManager...", flush=True)
    from omnitype.core.history_manager import HistoryManager
    hm = HistoryManager(db, cfg)
    hm.start_background_purge()
    print("  history_manager OK", flush=True)

    print("Step 7: AI Provider...", flush=True)
    from omnitype.ai.provider_factory import get_provider_factory
    try:
        provider = get_provider_factory().get_provider(cfg)
        print(f"  provider OK: {type(provider).__name__}", flush=True)
    except Exception as e:
        print(f"  provider FAILED (non-fatal): {e}", flush=True)

    print("Step 8: TriggerParser + Replacer...", flush=True)
    from omnitype.core.trigger_parser import TriggerParser
    from omnitype.core.replacer import TextReplacer
    tp = TriggerParser(cfg)
    tr = TextReplacer(cfg)
    print("  trigger_parser + replacer OK", flush=True)

    print("Step 9: NotificationWidget...", flush=True)
    from omnitype.ui.notification_widget import NotificationWidget
    nw = NotificationWidget()
    print("  notification OK", flush=True)

    print("Step 10: OmniTypeTray...", flush=True)
    from omnitype.ui.tray import OmniTypeTray
    tray = OmniTypeTray()
    tray.show()
    print("  tray OK (icon visible in tray)", flush=True)

    print("Step 11: KeyboardListener start...", flush=True)
    from omnitype.core.keyboard_listener import KeyboardListener
    kl = KeyboardListener(tp, lambda m: print(f"  trigger: {m.trigger_type}"), cfg)
    kl.start()
    print("  keyboard_listener started OK", flush=True)

    print("Step 12: brief idle (2s)...", flush=True)
    await asyncio.sleep(2)
    print("  idle OK", flush=True)

    print("Step 13: shutdown...", flush=True)
    kl.stop()
    hm.stop_background_purge()
    await db.close()
    tray.hide()
    print("  shutdown OK", flush=True)

    print("\n=== ALL STEPS PASSED ===", flush=True)
    app.quit()


print("Running diagnostic async loop...", flush=True)
with loop:
    try:
        loop.run_until_complete(diagnose())
    except Exception as exc:
        print(f"\nFATAL CRASH: {exc}", flush=True)
        traceback.print_exc()
        sys.exit(1)
