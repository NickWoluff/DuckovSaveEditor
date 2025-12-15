# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.win32.versioninfo import VSVersionInfo

block_cipher = None

a = Analysis(
    ['DuckovSaveEditor.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        ('version.txt', '.'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DuckovSaveEditor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='icon.ico',
    version='version_info.py',
)
