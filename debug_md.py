"""Debug markdown rendering pipeline."""
import markdown

md_text = "# Hello\n**World** *italic*"

# Test 1: basic
r1 = markdown.markdown(md_text)
print("basic:", r1)

# Test 2: with extensions
r2 = markdown.markdown(md_text, extensions=["nl2br", "fenced_code", "tables", "toc", "attr_list"])
print("with extensions:", r2)

# Now test the actual function from popup_window
import sys
sys.path.insert(0, ".")
from tinky.ui.popup.popup_window import _render_markdown, _build_output_html, _DARK

inner = _render_markdown(md_text)
print("_render_markdown output:", repr(inner[:200]))

html = _build_output_html(inner, _DARK)
print("Has <h1>:", "<h1>" in html)
print("Has <H1>:", "<H1>" in html)
print("HTML snippet:", html[html.find("<body>"):html.find("<body>")+300])
