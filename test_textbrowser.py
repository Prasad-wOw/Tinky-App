"""Test QTextBrowser rendering headings and styled HTML."""
import sys
from PySide6.QtWidgets import QApplication, QTextBrowser, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

app = QApplication(sys.argv)

win = QWidget()
win.setWindowTitle("QTextBrowser Markdown Test")
win.resize(700, 500)
lay = QVBoxLayout(win)

browser = QTextBrowser()
browser.setStyleSheet("""
    QTextBrowser {
        background-color: #0F0F18;
        color: #F0F0F0;
        border: none;
        font-family: "Segoe UI";
        font-size: 11pt;
        padding: 10px;
    }
""")

# Test: does QTextBrowser render <style> tags?
html_with_style = """<html>
<head>
<style>
body { background-color: #0F0F18; color: #F0F0F0; font-family: "Segoe UI"; font-size: 10.5pt; }
h1 { font-size: 16pt; font-weight: bold; color: #B39DDB; }
h2 { font-size: 13pt; color: #CE93D8; }
strong { font-weight: bold; color: #F0F0F0; }
em { font-style: italic; }
code { background-color: #1E1E30; color: #D4A0FF; }
</style>
</head>
<body>
<h1 id="test">H1 Heading — Should be Purple/Large</h1>
<h2>H2 Heading</h2>
<p><strong>Bold text</strong> and <em>italic text</em></p>
<p>Normal paragraph text in Segoe UI.</p>
<ul>
<li>List item 1</li>
<li>List item 2</li>
</ul>
<pre><code>def hello():
    print("code block")</code></pre>
</body>
</html>"""

browser.setHtml(html_with_style)
lay.addWidget(browser)
win.show()

print("Window shown - check if:")
print("1. H1 is styled (purple, large)")
print("2. Bold/italic render")
print("3. Code block appears")

def done():
    print("Test window closed.")
    app.quit()

QTimer.singleShot(8000, done)
app.exec()
