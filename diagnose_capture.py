"""
Standalone capture diagnostic (updated sentinel fix).
Run this, select text in any other window, then press F9.
"""
import sys
import ctypes
import ctypes.wintypes
import time
import uuid
import threading

print("Capture Diagnostic v2 (UUID sentinel, keyboard.send)")
print("1. Open any app (Notepad, Chrome, etc.)")
print("2. Select some text")  
print("3. Press F9 while that app is focused")
print("4. Wait ~2 seconds for result")
print()

user32 = ctypes.windll.user32

def get_clipboard():
    try:
        import pyperclip
        return pyperclip.paste() or ""
    except Exception as e:
        print(f"  pyperclip.paste() FAILED: {e}")
        return ""

def set_clipboard(text):
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"  pyperclip.copy() FAILED: {e}")
        return False

def capture_test(hwnd):
    print(f"\n=== CAPTURE TEST (hwnd={hwnd:#010x}) ===")

    old_clip = get_clipboard()
    print(f"  [1] Old clipboard: {repr(old_clip[:50])}")

    sentinel = f"TINKY_SENTINEL_{uuid.uuid4().hex}"
    ok = set_clipboard(sentinel)
    time.sleep(0.02)
    verify = get_clipboard()
    print(f"  [2] Sentinel written: {ok}, read-back matches: {verify == sentinel}")

    fg = user32.GetForegroundWindow()
    print(f"  [3] Current foreground: {fg:#010x}, target: {hwnd:#010x}")

    # Restore focus to source window
    if fg != hwnd:
        print(f"  [3b] Restoring focus to source window...")
        user32.AllowSetForegroundWindow(0xFFFFFFFF)
        user32.SetForegroundWindow(hwnd)
        time.sleep(0.06)
        fg2 = user32.GetForegroundWindow()
        print(f"  [3c] Foreground after restore: {fg2:#010x}, match: {fg2 == hwnd}")
    else:
        time.sleep(0.06)

    print("  [4] Sending Ctrl+C via keyboard.send()...")
    try:
        import keyboard as kb
        kb.send("ctrl+c")
        print("  [4] keyboard.send('ctrl+c') completed")
    except Exception as e:
        print(f"  [4] keyboard.send FAILED: {e}")

    delays_ms = [60, 80, 100, 130, 160, 200, 250, 300]
    captured = ""
    for d in delays_ms:
        time.sleep(d / 1000)
        val = get_clipboard()
        print(f"  [5] After {d:3d}ms: {repr(val[:50])}")
        if val and val != sentinel:
            captured = val
            print(f"  ✓ CAPTURED {len(captured)} chars!")
            break
    
    if not captured:
        print("  ✗ NOTHING captured after all retries")
        print("  Possible causes:")
        print("    - No text was selected")
        print("    - App doesn't support Ctrl+C via keyboard.send()")
        print("    - Focus wasn't restored to source window")

    set_clipboard(old_clip)
    print(f"  [6] Restored clipboard.")
    print(f"  RESULT: {repr(captured[:100])}")
    print("=== END ===\n")

def on_f9():
    hwnd = user32.GetForegroundWindow()
    print(f"\nF9 pressed! Foreground: {hwnd:#010x}")

    def thread_fn():
        time.sleep(0.15)   # same delay as real app
        capture_test(hwnd)

    threading.Thread(target=thread_fn, daemon=True).start()

import keyboard as kb
kb.add_hotkey("f9", on_f9, suppress=False)
print("Listening for F9 (press Esc to quit)...")
kb.wait("esc")
print("Goodbye.")
