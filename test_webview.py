"""Diagnostic: test QWebEngineView in a WA_TranslucentBackground frameless window."""
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

win = QWidget()
win.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
win.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
win.resize(700, 500)

lay = QVBoxLayout(win)
lay.setContentsMargins(0, 0, 0, 0)

web = QWebEngineView()
web.page().setBackgroundColor(QColor("#0D0D14"))

html = """<!DOCTYPE html>
<html><head><style>
body { background: #0D0D14; color: #F0F0F0; font-size: 16pt; padding: 20px; }
h1 { color: #B39DDB; }
</style></head><body>
<h1>TEST H1 HEADING</h1>
<p><strong>Bold text</strong> and <em>italic text</em></p>
<p>If you can read this, QWebEngineView is working.</p>
</body></html>"""

web.setHtml(html)
lay.addWidget(web)
win.show()

print("Window visible:", win.isVisible())
print("WebView visible:", web.isVisible())
print("WebView size:", web.size())

def check():
    print("WebView title:", web.title())
    print("DONE - check if window shows content")
    app.quit()

QTimer.singleShot(3000, check)
app.exec()
