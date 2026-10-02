# -*- mode: python ; coding: utf-8 -*-
"""
OmniType.spec
~~~~~~~~~~~~~
PyInstaller spec file for building the OmniType Windows executable.

Usage
-----
    pyinstaller OmniType.spec

Produces a single-file, no-console .exe in dist/OmniType.exe.
"""

block_cipher = None

a = Analysis(
    ["omnitype/main.py"],
    pathex=["d:/Abode/VIT/Capstone/OmniType"],
    binaries=[],
    datas=[
        # Default config shipped with the package
        ("config.default.toml", "."),
        # Application assets (icons, images, etc.)
        ("assets", "assets"),
    ],
    hiddenimports=[
        # PySide6 Qt modules
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PySide6.QtGui",
        "PySide6.QtNetwork",
        "PySide6.QtSvg",
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
        "pywintypes",
        "psutil",
        # Database
        "sqlite3",
        # Config / serialisation
        "tomllib",
        "tomli",
        "tomli_w",
        # OmniType submodules (ensure nothing is tree-shaken away)
        "omnitype.app",
        "omnitype.main",
        "omnitype.core.keyboard_listener",
        "omnitype.core.trigger_parser",
        "omnitype.core.text_capture",
        "omnitype.core.replacer",
        "omnitype.core.undo_manager",
        "omnitype.core.history_manager",
        "omnitype.storage.config",
        "omnitype.storage.database",
        "omnitype.ai.base_provider",
        "omnitype.ai.gemini_provider",
        "omnitype.ai.openai_provider",
        "omnitype.ai.cloudflare_provider",
        "omnitype.ai.ollama_provider",
        "omnitype.ai.provider_factory",
        "omnitype.ui.tray",
        "omnitype.ui.settings_window",
        "omnitype.ui.history_window",
        "omnitype.ui.notification_widget",
        "omnitype.security.encryption",
        "omnitype.utils.logger",
        "omnitype.utils.helpers",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Heavy scientific libraries not needed at runtime
        "tkinter",
        "matplotlib",
        "scipy",
        "numpy",
        "pandas",
        "PIL",
        "cv2",
        # Test frameworks
        "pytest",
        "unittest",
        # IPython / Jupyter
        "IPython",
        "jupyter",
        # Avoid pulling in the entire Qt test suite
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
    name="OmniType",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        # UPX can corrupt some DLLs — exclude Qt and crypto ones to be safe
        "vcruntime*.dll",
        "VCRUNTIME*.dll",
        "Qt6*.dll",
        "PySide6/*.pyd",
        "cryptography*.pyd",
    ],
    runtime_tmpdir=None,
    # No console window — OmniType is a tray/GUI application
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Application icon
    icon="assets/icon.ico",
    # Windows version info (optional .rc or version tuple)
    version=None,
)
