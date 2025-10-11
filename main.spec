# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/style.qss', 'assets'),
        ('assets/cd_placeholder.png', 'assets'),
        ('assets/shuffle_red.png', 'assets'),
        ('assets/shuffle_orange.png', 'assets'),
        ('assets/supported_sites.txt', 'assets'),
        # Add any other assets you use
    ],
    hiddenimports=['pygame', 'PyQt6', 'mutagen', 'mutagen.mp3', 'mutagen.easyid3', 'mutagen.id3', 'pyttsx3','yt_dlp'],
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
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
