"""
convert_icons.py
~~~~~~~~~~~~~~~~
Convert PNG icons to ICO format for PyInstaller.

Place these files in d:\Abode\VIT\Capstone\OmniType\assets\ first:
  - tinky_app_icon.png   (the dark blue rounded-square icon)
  - tinky_tray_icon.png  (the circular light icon)

Then run:  python convert_icons.py
"""

from PIL import Image
import os

ASSETS = os.path.join(os.path.dirname(__file__), "assets")

def png_to_ico(src_png: str, dst_ico: str) -> None:
    """Convert a PNG to a multi-resolution ICO file."""
    img = Image.open(src_png).convert("RGBA")
    sizes = [(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)]
    icons = []
    for sz in sizes:
        resized = img.resize(sz, Image.LANCZOS)
        icons.append(resized)
    icons[0].save(dst_ico, format="ICO", sizes=[s for s in sizes], append_images=icons[1:])
    print(f"  ✓  {os.path.basename(src_png)} → {os.path.basename(dst_ico)}")

def png_to_png_resized(src_png: str, dst_png: str, size: int = 256) -> None:
    """Resize and save PNG for tray icon use."""
    img = Image.open(src_png).convert("RGBA")
    img = img.resize((size, size), Image.LANCZOS)
    img.save(dst_png, format="PNG")
    print(f"  ✓  {os.path.basename(src_png)} → {os.path.basename(dst_png)} ({size}x{size})")

if __name__ == "__main__":
    print("Converting icons...")

    app_png  = os.path.join(ASSETS, "tinky_app_icon.png")
    app_ico  = os.path.join(ASSETS, "tinky_app_icon.ico")
    tray_png = os.path.join(ASSETS, "tinky_tray_icon.png")
    tray_out = os.path.join(ASSETS, "tinky_tray_256.png")

    if not os.path.exists(app_png):
        print(f"ERROR: {app_png} not found.")
        print("  → Save the dark-background app icon as 'tinky_app_icon.png' in assets/")
        exit(1)

    if not os.path.exists(tray_png):
        print(f"ERROR: {tray_png} not found.")
        print("  → Save the circular tray icon as 'tinky_tray_icon.png' in assets/")
        exit(1)

    png_to_ico(app_png, app_ico)
    png_to_png_resized(tray_png, tray_out, size=256)

    # Also copy tray as 32x32 for hi-dpi
    tray_32 = os.path.join(ASSETS, "tinky_tray_32.png")
    png_to_png_resized(tray_png, tray_32, size=32)

    print("\nDone! Now run:  python -m PyInstaller --clean --noconfirm Tinky.spec")
