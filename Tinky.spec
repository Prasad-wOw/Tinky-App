# -*- mode: python ; coding: utf-8 -*-
"""
Tinky.spec
~~~~~~~~~~~
PyInstaller spec file for building the Tinky Windows executable.

Usage
-----
    pyinstaller Tinky.spec

Produces a single-file, no-console Tinky.exe in dist/.
"""

block_cipher = None

import os

# Check if assets directory exists (it's optional)
_assets_exists = os.path.isdir("assets")

a = Analysis(
    ["tinky/main.py"],
    pathex=["d:/Abode/VIT/Capstone/OmniType"],
    binaries=[],
    datas=[
        ("config.default.toml", "."),
    ] + ([("assets", "assets")] if _assets_exists else []),
    hiddenimports=[
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PySide6.QtGui",
        "PySide6.QtNetwork",
        "PySide6.QtSvg",
        # NOTE: QtWebEngineWidgets deliberately excluded — we use QTextBrowser
        #       to avoid z-ordering bugs in frameless translucent windows.
        # Async / event-loop
        "qasync",
        "asyncio",
        "aiohttp",
        "aiosqlite",
        # Input / output
        "keyboard",
        "pyperclip",
        "pyautogui",
        "pynput",
        "pynput.keyboard",
        "pynput.mouse",
        # Crypto
        "cryptography",
        "cryptography.fernet",
        "cryptography.hazmat.primitives",
        "cryptography.hazmat.backends",
        # Windows API
        "win32api",
        "win32gui",
        "win32process",
        "win32con",
        "win32clipboard",
        "pywintypes",
        "pythoncom",
        # COM automation (used for Word/Excel/Outlook text capture)
        "win32com",
        "win32com.client",
        "win32com.server",
        "win32com.client.dynamic",
        "win32com.client.gencache",
        # Database
        "sqlite3",
        # Config / serialisation
        "tomllib",
        "tomli_w",
        # Markdown rendering — popup output via QTextBrowser
        "markdown",
        "markdown.core",
        "markdown.preprocessors",
        "markdown.blockparser",
        "markdown.blockprocessors",
        "markdown.treeprocessors",
        "markdown.inlinepatterns",
        "markdown.postprocessors",
        "markdown.extensions",
        "markdown.extensions.nl2br",
        "markdown.extensions.fenced_code",
        "markdown.extensions.tables",
        "markdown.extensions.toc",
        "markdown.extensions.attr_list",
        "markdown.extensions.def_list",
        "markdown.extensions.abbr",
        # tinky submodules (ensure nothing is tree-shaken away)
        "tinky.app",
        "tinky.main",
        "tinky.core.keyboard_listener",
        "tinky.core.trigger_parser",
        "tinky.core.replacer",
        "tinky.core.undo_manager",
        "tinky.core.history_manager",
        "tinky.core.hotkey_manager",
        "tinky.core.selection_capture",
        "tinky.storage.config",
        "tinky.storage.database",
        "tinky.ai.base_provider",
        "tinky.ai.gemini_provider",
        "tinky.ai.openai_provider",
        "tinky.ai.cloudflare_provider",
        "tinky.ai.ollama_provider",
        "tinky.ai.openrouter_provider",
        "tinky.ai.provider_factory",
        "tinky.ui.tray",
        "tinky.ui.widgets",
        "tinky.ui.dashboard",
        "tinky.ui.settings_window",
        "tinky.ui.history_window",
        "tinky.ui.notification_widget",
        "tinky.ui.popup.popup_window",
        "tinky.ui.popup.actions",
        "tinky.security.encryption",
        "tinky.utils.logger",
        "tinky.utils.helpers",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter",
        "matplotlib",
        "scipy",
        "numpy",
        "pandas",
        "PIL",
        "cv2",
        "pytest",
        "unittest",
        "IPython",
        "jupyter",
        "PySide6.QtTest",
        "PySide6.QtBluetooth",
        "PySide6.Qt3DCore",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="Tinky",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        "vcruntime*.dll",
        "VCRUNTIME*.dll",
        "Qt6*.dll",
        "PySide6/*.pyd",
        "cryptography*.pyd",
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/tinky_app_icon.ico" if _assets_exists and os.path.isfile("assets/tinky_app_icon.ico") else
         ("assets/icon.ico" if _assets_exists and os.path.isfile("assets/icon.ico") else None),
    version=None,
)
