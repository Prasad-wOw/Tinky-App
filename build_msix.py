import os
import sys
import glob
import shutil
import subprocess
from PIL import Image

# 1. Config
APP_NAME = "Tinky_"  # Make sure this exactly matches the name you reserved in Partner Center
IDENTITY_NAME = "Vipluv.Tinky"
APP_VERSION = "1.0.7.0"
PUBLISHER = "CN=5BF16E98-855F-4B3B-8288-3AE6CCAC3A27"
PUBLISHER_DISPLAY_NAME = "Vipluv"
TARGET_ARCH = "x64"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = os.path.join(BASE_DIR, "msix_staging")
ASSETS_DIR = os.path.join(STAGING_DIR, "Assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "installer_output")

SOURCE_ICON = os.path.join(BASE_DIR, "assets", "Tinky_Ultimate.png")
SOURCE_DIST = os.path.join(BASE_DIR, "dist_release", "main.dist")  # standalone dist folder

# We package the full Nuitka standalone dist folder so python313.dll sits
# right next to Tinky.exe inside the MSIX. This avoids the onefile self-extraction
# temp-dir issue that causes 'python313.dll not found' on fresh machines.

# 2. Setup Staging — clean then copy full standalone dist
if os.path.exists(STAGING_DIR):
    shutil.rmtree(STAGING_DIR)
os.makedirs(STAGING_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Copy entire standalone dist into staging root
if not os.path.isdir(SOURCE_DIST):
    print(f"ERROR: Standalone dist folder not found: {SOURCE_DIST}")
    print("Run build_nuitka.ps1 first (it produces both Tinky.exe onefile AND main.dist folder).")
    raise SystemExit(1)

print(f"Copying standalone dist ({SOURCE_DIST}) into MSIX staging...")
for item in os.listdir(SOURCE_DIST):
    s = os.path.join(SOURCE_DIST, item)
    d = os.path.join(STAGING_DIR, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)
print(f"  Copied {len(os.listdir(SOURCE_DIST))} items from dist folder.")

# Now create the MSIX Assets folder (uppercase — different from dist's 'assets' folder)
os.makedirs(ASSETS_DIR, exist_ok=True)

# 3. Generate Assets
print("Generating MSIX assets from:", SOURCE_ICON)
img = Image.open(SOURCE_ICON).convert("RGBA")

assets = {
    "Square44x44Logo.png": (44, 44),
    "Square44x44Logo.targetsize-44_altform-unplated.png": (44, 44),
    "Square150x150Logo.png": (150, 150),
    "Square310x310Logo.png": (310, 310),
    "Wide310x150Logo.png": (310, 150),
    "StoreLogo.png": (50, 50),
    "SplashScreen.png": (620, 300),
}

for name, size in assets.items():
    # If aspect ratio is not 1:1, we should paste the image centered on a transparent background
    if size[0] != size[1]:
        bg = Image.new("RGBA", size, (255, 255, 255, 0))
        # scale icon to fit height
        scale = size[1] / img.size[1]
        new_w, new_h = int(img.size[0] * scale), int(img.size[1] * scale)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        offset_x = (size[0] - new_w) // 2
        offset_y = (size[1] - new_h) // 2
        bg.paste(resized, (offset_x, offset_y))
        out = bg
    else:
        out = img.resize(size, Image.Resampling.LANCZOS)
        
    out.save(os.path.join(ASSETS_DIR, name))

# 4. Generate AppxManifest.xml
print("Generating AppxManifest.xml")
manifest = f"""<?xml version="1.0" encoding="utf-8"?>
<Package
  xmlns="http://schemas.microsoft.com/appx/manifest/foundation/windows10"
  xmlns:uap="http://schemas.microsoft.com/appx/manifest/uap/windows10"
  xmlns:desktop="http://schemas.microsoft.com/appx/manifest/desktop/windows10"
  xmlns:rescap="http://schemas.microsoft.com/appx/manifest/foundation/windows10/restrictedcapabilities"
  IgnorableNamespaces="uap desktop rescap">

  <Identity
    Name="{IDENTITY_NAME}"
    Publisher="{PUBLISHER}"
    Version="{APP_VERSION}"
    ProcessorArchitecture="{TARGET_ARCH}" />

  <Properties>
    <DisplayName>{APP_NAME}</DisplayName>
    <PublisherDisplayName>{PUBLISHER_DISPLAY_NAME}</PublisherDisplayName>
    <Logo>Assets\\StoreLogo.png</Logo>
  </Properties>

  <Dependencies>
    <TargetDeviceFamily Name="Windows.Desktop" MinVersion="10.0.17763.0" MaxVersionTested="10.0.22621.0" />
    <!-- Visual C++ Runtime — silently auto-installed by the Store if missing. Zero added size to MSIX. -->
    <PackageDependency
        Name="Microsoft.VCLibs.140.00"
        MinVersion="14.0.0.0"
        Publisher="CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US" />
    <PackageDependency
        Name="Microsoft.VCLibs.140.00.UWPDesktop"
        MinVersion="14.0.0.0"
        Publisher="CN=Microsoft Corporation, O=Microsoft Corporation, L=Redmond, S=Washington, C=US" />
  </Dependencies>

  <Resources>
    <Resource Language="en-us" />
  </Resources>

  <Applications>
    <Application Id="TinkyApp"
      Executable="Tinky.exe"
      EntryPoint="Windows.FullTrustApplication">
      <uap:VisualElements
        DisplayName="Tinky"
        Description="Your Digital AI Genie"
        BackgroundColor="transparent"
        Square150x150Logo="Assets\\Square150x150Logo.png"
        Square44x44Logo="Assets\\Square44x44Logo.png">
        <uap:DefaultTile Wide310x150Logo="Assets\\Wide310x150Logo.png" Square310x310Logo="Assets\\Square310x310Logo.png" />
        <uap:SplashScreen Image="Assets\\SplashScreen.png" />
      </uap:VisualElements>
      <Extensions>
        <desktop:Extension Category="windows.startupTask" Executable="Tinky.exe" EntryPoint="Windows.FullTrustApplication">
          <desktop:StartupTask TaskId="TinkyStartup" Enabled="true" DisplayName="Tinky" />
        </desktop:Extension>
      </Extensions>
    </Application>
  </Applications>

  <Capabilities>
    <rescap:Capability Name="runFullTrust" />
  </Capabilities>
</Package>
"""
with open(os.path.join(STAGING_DIR, "AppxManifest.xml"), "w", encoding="utf-8") as f:
    f.write(manifest)

# 5. Find makeappx.exe
makeappx = None
sdk_paths = glob.glob(r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.*\x64\makeappx.exe")
if sdk_paths:
    makeappx = sorted(sdk_paths)[-1]  # get latest SDK version

if not makeappx:
    print("Error: Could not find makeappx.exe in Windows Kits directory. Is the Windows SDK installed?")
    sys.exit(1)

# 6. Pack MSIX
out_msix = os.path.join(OUTPUT_DIR, f"Tinky_{APP_VERSION}_{TARGET_ARCH}.msix")
if os.path.exists(out_msix):
    os.remove(out_msix)

cmd = [
    makeappx, "pack",
    "/d", STAGING_DIR,
    "/p", out_msix,
    "/o"
]

print(f"Running makeappx: {' '.join(cmd)}")
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("makeappx failed:")
    print(result.stdout)
    print(result.stderr)
    sys.exit(1)

print(f"\nSuccess! MSIX created at: {out_msix}")
print("\nTo test locally, you must sign it with a trusted certificate, or submit it to the Microsoft Store (they will sign it).")


