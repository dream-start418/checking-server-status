# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for ServerStatusChecker
This ensures win10toast and pywin32 are properly bundled
"""

a = Analysis(
    ['server_status_checker_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'win10toast',
        'win32api',
        'win32gui',
        'win32con',
        'win32process',
        'pywintypes',
        'win32timezone',
        'requests',
        'sqlite3',
        'server_status_checker',  # Include the checker module
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    collect_submodules=['win32api', 'win32gui', 'win32con', 'win32process'],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ServerStatusChecker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI only)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
