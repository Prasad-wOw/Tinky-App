"""
generate_icon.py
~~~~~~~~~~~~~~~~
Generates the OmniType application icon (icon.ico) programmatically.
Creates a 256x256 purple circle with a white "O" letter.
Requires: Pillow  (pip install pillow)
"""

import sys
from pathlib import Path


def generate_icon() -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not found. Trying to create icon without it...")
        _generate_with_pyside6()
        return

    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Purple circle background
        margin = max(1, size // 16)
        draw.ellipse(
            [margin, margin, size - margin, size - margin],
            fill=(124, 58, 237, 255),  # #7C3AED
        )

        # White "O" letter — scale font size to image
        font_size = int(size * 0.55)
        try:
            font = ImageFont.truetype("segoeui.ttf", font_size)
        except (IOError, OSError):
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except (IOError, OSError):
                font = ImageFont.load_default()

        text = "O"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (size - text_w) // 2 - bbox[0]
        y = (size - text_h) // 2 - bbox[1]
        draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

        images.append(img)

    out_path = Path(__file__).parent / "assets" / "icon.ico"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        out_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=images[1:],
    )
    print(f"Icon saved to: {out_path}")


def _generate_with_pyside6() -> None:
    """Fallback: generate icon using PySide6 QPainter."""
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtGui import (
            QBrush,
            QColor,
            QFont,
            QFontMetricsF,
            QImage,
            QPainter,
            QRadialGradient,
        )
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("PySide6 not found either. Skipping icon generation.")
        return

    app = QApplication.instance() or QApplication(sys.argv)

    size = 256
    img = QImage(size, size, QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(Qt.GlobalColor.transparent)

    painter = QPainter(img)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Purple filled circle
    painter.setBrush(QBrush(QColor("#7C3AED")))
    painter.setPen(Qt.PenStyle.NoPen)
    margin = 8
    painter.drawEllipse(margin, margin, size - 2 * margin, size - 2 * margin)

    # White "O"
    font = QFont("Segoe UI", int(size * 0.5), QFont.Weight.Bold)
    painter.setFont(font)
    painter.setPen(QColor("#FFFFFF"))
    painter.drawText(img.rect(), Qt.AlignmentFlag.AlignCenter, "O")

    painter.end()

    out_path = Path(__file__).parent / "assets" / "icon.ico"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Save as PNG then convert via pillow, or save as BMP fallback
    png_path = out_path.with_suffix(".png")
    img.save(str(png_path))

    try:
        from PIL import Image
        pil_img = Image.open(str(png_path))
        pil_img.save(str(out_path), format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
        png_path.unlink(missing_ok=True)
        print(f"Icon saved to: {out_path}")
    except ImportError:
        print(f"Icon saved as PNG (no ICO): {png_path}")


if __name__ == "__main__":
    generate_icon()
