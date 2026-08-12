# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[('C:/Users/sametucak/AppData/Local/anaconda3/Library/bin/libexpat.dll', '.'), ('C:/Users/sametucak/AppData/Local/anaconda3/Library/bin/ffi.dll', '.'), ('C:/Users/sametucak/AppData/Local/anaconda3/Library/bin/tcl86t.dll', '.'), ('C:/Users/sametucak/AppData/Local/anaconda3/Library/bin/tk86t.dll', '.')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BNS-1.0.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BNS-1.0.0',
)
