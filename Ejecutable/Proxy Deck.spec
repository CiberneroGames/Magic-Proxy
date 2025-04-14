# Proxy Deck.spec

block_cipher = None

a = Analysis(
    ['proxy_deck.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('deck_example.txt', '.'), 
        ('README.txt', '.'), 
        ('magic.ico', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='Proxy Deck',
    icon='magic.ico',
    debug=False,
    strip=False,
    upx=True,
    console=True,  # Cambialo a False si no querés que aparezca la consola
)
