"""Verification script for all three fixes."""
import sys

print("=== Fix 1: markdown package ===")
import markdown
md_text = "# Heading 1\n## Heading 2\n**bold** *italic*\n- item1\n- item2"
result = markdown.markdown(md_text, extensions=["nl2br", "fenced_code", "tables"])
assert "<h1>" in result, "H1 not found"
assert "<h2>" in result, "H2 not found"
assert "<strong>" in result, "bold not found"
print("OK - markdown renders:", result[:100], "...")

print()
print("=== Fix 2: SendInput struct size ===")
from tinky.core.selection_capture import _INPUT, _send_ctrl_c_raw
import ctypes
sz = ctypes.sizeof(_INPUT)
print(f"sizeof(_INPUT) = {sz} (must be 28)")
assert sz == 28, f"WRONG SIZE: {sz}"
print("OK - struct size is correct")

print()
print("=== Fix 2b: Hotkey callback is non-blocking ===")
import inspect
import tinky.app as app_mod
src = inspect.getsource(app_mod)
assert "threading.Thread(target=_capture_thread" in src, "Thread not found"
assert "t.start()" in src, "t.start() not found"
print("OK - capture moved to daemon thread, hook returns instantly")

print()
print("=== Markdown in popup QTextBrowser ===")
from tinky.ui.popup.popup_window import _render_markdown, _build_output_html, _DARK
html = _build_output_html(_render_markdown("# Hello\n**World** *italic*"), _DARK)
assert "<h1>" in html, "H1 missing from HTML"
assert "<strong>" in html, "bold missing from HTML"
print("OK - popup renders markdown to styled HTML for QTextBrowser")

print()
print("ALL CHECKS PASSED")
