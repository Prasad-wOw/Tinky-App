"""Save and convert uploaded Tinky icons to assets/."""
from PIL import Image
import shutil, os, sys

BRAIN = r"C:\Users\Narasimha Prasad\.gemini\antigravity\brain\864eeabd-b569-467f-ba34-741e92fe4a3d"
ASSETS = r"d:\Abode\VIT\Capstone\OmniType\assets"

# media__1780767610563.png = 906 KB = tinky_app_icon (dark bg, large)
# media__1780767484982.png = 221 KB = tinky_tray_icon (circular light)
APP_SRC  = os.path.join(BRAIN, "media__1780767610563.png")
TRAY_SRC = os.path.join(BRAIN, "media__1780767484982.png")

def save_png(src, dst_name):
    dst = os.path.join(ASSETS, dst_name)
    shutil.copy2(src, dst)
    img = Image.open(dst)
    print(f"  Copied {dst_name}: {img.size}, mode={img.mode}")
    return dst

def png_to_ico(src_png, dst_ico):
    img = Image.open(src_png).convert("RGBA")
    sizes = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
    ico_images = [img.resize(s, Image.LANCZOS) for s in sizes]
    ico_images[0].save(
        dst_ico, format="ICO",
        sizes=sizes,
        append_images=ico_images[1:]
    )
    sz = os.path.getsize(dst_ico)
    print(f"  Created ICO: {os.path.basename(dst_ico)} ({sz//1024} KB)")

def resize_png(src, dst, size):
    img = Image.open(src).convert("RGBA")
    img = img.resize((size,size), Image.LANCZOS)
    img.save(dst, "PNG")
    print(f"  Resized PNG: {os.path.basename(dst)} ({size}x{size})")

print("=== Tinky Icon Setup ===\n")

# 1. Save raw PNGs
app_png  = save_png(APP_SRC,  "tinky_app_icon.png")
tray_png = save_png(TRAY_SRC, "tinky_tray_icon.png")

# 2. Convert app icon → ICO (multi-resolution for exe)
app_ico = os.path.join(ASSETS, "tinky_app_icon.ico")
png_to_ico(app_png, app_ico)

# 3. Resize tray icon to standard sizes
resize_png(tray_png, os.path.join(ASSETS, "tinky_tray_256.png"), 256)
resize_png(tray_png, os.path.join(ASSETS, "tinky_tray_32.png"),  32)

print("\nAssets directory:")
for f in sorted(os.listdir(ASSETS)):
    p = os.path.join(ASSETS, f)
    print(f"  {f:40s}  {os.path.getsize(p)//1024:4d} KB")

print("\n✓ All icons ready. Now rebuild with:")
print("  python -m PyInstaller --clean --noconfirm Tinky.spec")
