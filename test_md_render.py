"""Live visual test of markdown rendering in QTextBrowser with popup's CSS."""
import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextBrowser
from PySide6.QtCore import QTimer
import markdown

sys.path.insert(0, ".")
from tinky.ui.popup.popup_window import _render_markdown, _build_output_html, _apply_output_style, _DARK

app = QApplication(sys.argv)

win = QWidget()
win.setWindowTitle("Markdown Rendering Test - should show styled headings/bold/code")
win.resize(750, 600)
win.setStyleSheet("background: #0F0F18;")

lay = QVBoxLayout(win)
lay.setContentsMargins(0, 0, 0, 0)

browser = QTextBrowser()
browser.setStyleSheet("QTextBrowser { background: #0F0F18; border: none; padding: 10px; }")

# Apply our CSS
_apply_output_style(browser)

# Render a rich markdown sample
sample_md = """# Main Heading (H1) — Should be large & purple
## Section Heading (H2) — should be lighter purple

This is a normal paragraph with **bold text**, *italic text*, and `inline code`.

### Subsection (H3)

- List item one
- List item two
- List item three

Here is a code block:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Tinky"))
```

| Column A | Column B | Column C |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

> This is a blockquote. It should have a purple left border.

---
Normal text after horizontal rule.
"""

inner = _render_markdown(sample_md)
html = _build_output_html(inner, _DARK)

_apply_output_style(browser)
browser.setHtml(html)
_apply_output_style(browser)  # re-apply after setHtml resets doc

lay.addWidget(browser)
win.show()

print("=== Check the window for:")
print("  H1: Large, purple (#B39DDB)")
print("  H2: Medium, lighter purple (#CE93D8)")
print("  H3: Small bold lavender (#E1BEE7)")
print("  **bold** -> bold text")
print("  *italic* -> italic text")
print("  `code` -> purple monospace on dark bg")
print("  ```block``` -> dark code block")
print("  Table -> bordered")
print("  > blockquote -> grey with left border")

def done():
    app.quit()
QTimer.singleShot(15000, done)
app.exec()
print("Done.")
