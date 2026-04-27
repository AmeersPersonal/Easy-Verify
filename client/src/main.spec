# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_all

# Collect all metadata and binaries for the heavy hitters
datas_df, binaries_df, hidden_df = collect_all('deepface')
datas_tf, binaries_tf, hidden_tf = collect_all('tensorflow')
datas_tk, binaries_tk, hidden_tk = collect_all('tf_keras')
datas_rf, binaries_rf, hidden_rf = collect_all('retina_face')

block_cipher = None

# Combine all data
all_datas = datas_df + datas_tf + datas_tk + datas_rf + [
    ('assets', 'assets'),
    ('deepface/*.h5', 'deepface_weights')
]

# Combine all hidden imports
all_hidden = hidden_df + hidden_tf + hidden_tk + hidden_rf + [
    'cv2',
    'pandas',
    'tf_keras',
    'keras.api._v2.keras'
]


added_files = datas_df + datas_tf + [
    ('assets', 'assets'), ('deepface/*.h5', 'deepface_weights')
];

a = Analysis(
    ['main.pyw'],
    pathex=[],
    binaries=binaries_df + binaries_tf + binaries_rf,
    datas=all_datas,
    hiddenimports=all_hidden,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set this to true if you want to read the console output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
