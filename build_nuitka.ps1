# build_nuitka.ps1
# Compiles Tinky into a standalone, release-ready Windows executable using Nuitka.
# Usage: .\build_nuitka.ps1
#
# IMPORTANT: This script must be run using Python from python.org (NOT Windows Store Python).
# Windows Store Python (PythonSoftwareFoundation.Python.3.13) installs python313.dll in a
# restricted app package folder that Nuitka cannot bundle, causing crashes on other machines.
# To verify which Python you are using, run: (Get-Command python).Source
# It should point to somewhere like C:\Python313\python.exe, NOT AppData\Local\Microsoft\WindowsApps\

$ErrorActionPreference = "Stop"
$ROOT   = $PSScriptRoot
$ASSETS = Join-Path $ROOT "assets"
$ICON   = Join-Path $ASSETS "tinky_app_icon.ico"
$OUT    = Join-Path $ROOT "dist_release"

Write-Host "=== Tinky Nuitka Build ===" -ForegroundColor Cyan
Write-Host "Root   : $ROOT"
Write-Host "Output : $OUT"

# Kill any running instance before overwriting the exe
Stop-Process -Name "Tinky" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Clean previous output
if (Test-Path $OUT) {
    Remove-Item -Recurse -Force $OUT
    Start-Sleep -Seconds 3  # Wait for Windows to fully release file handles
}
New-Item -ItemType Directory -Force -Path $OUT | Out-Null

py -m nuitka `
    --standalone `
    --onefile `
    "--onefile-tempdir-spec={CACHE_DIR}/Tinky/Runtime" `
    --windows-console-mode=disable `
    "--windows-icon-from-ico=$ICON" `
    --output-dir="$OUT" `
    --output-filename="Tinky.exe" `
    --company-name="Tinky" `
    --product-name="Tinky" `
    --file-version="1.0.0.0" `
    --product-version="1.0.0.0" `
    "--file-description=Tinky - Your Digital AI Genie" `
    `
    --enable-plugin=pyside6 `
    `
    "--include-data-dir=$ASSETS=assets" `
    "--include-data-files=$ROOT\config.default.toml=config.default.toml" `
    `
    --include-package=tinky `
    --include-package=qasync `
    --include-package=aiohttp `
    --include-package=aiosqlite `
    --include-package=keyboard `
    --include-package=pyperclip `
    --include-package=pyautogui `
    --include-package=pynput `
    --include-package=cryptography `
    --include-package=markdown `
    --include-package=tomli_w `
    --include-package=win32api `
    --include-package=win32gui `
    --include-package=win32process `
    --include-package=win32con `
    --include-package=win32clipboard `
    --include-package=pythoncom `
    --include-package=win32com `
    --include-package=pywintypes `
    --include-package=winrt `
    `
    --nofollow-import-to=tkinter `
    --nofollow-import-to=matplotlib `
    --nofollow-import-to=scipy `
    --nofollow-import-to=pandas `
    --nofollow-import-to=PIL `
    --nofollow-import-to=cv2 `
    --nofollow-import-to=pytest `
    --nofollow-import-to=pytest_asyncio `
    --nofollow-import-to=_pytest `
    --nofollow-import-to=IPython `
    --nofollow-import-to=jupyter `
    --nofollow-import-to=setuptools `
    --nofollow-import-to=distutils `
    --nofollow-import-to=unittest `
    --nofollow-import-to=win32com.test `
    --nofollow-import-to=win32com.server.util `
    --nofollow-import-to=docutils `
    --nofollow-import-to=sphinx `
    --nofollow-import-to=pygments `
    --nofollow-import-to=pydoc `
    `
    --assume-yes-for-downloads `
    --python-flag=no_site `
    "$ROOT\tinky\main.py"

if ($LASTEXITCODE -eq 0) {
    $exe    = Join-Path $OUT "Tinky.exe"
    $sizeMB = [math]::Round((Get-Item $exe).Length / 1MB, 1)
    Write-Host ""
    Write-Host "=== BUILD SUCCESSFUL ===" -ForegroundColor Green
    Write-Host "Executable : $exe ($sizeMB MB)" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "=== BUILD FAILED (exit $LASTEXITCODE) ===" -ForegroundColor Red
    exit 1
}
