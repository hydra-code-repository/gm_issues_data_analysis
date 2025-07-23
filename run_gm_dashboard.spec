from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None

a = Analysis(
    ['run_gm_dashboard.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        (
            r"gm_dashboard_env\Lib\site-packages\altair\vegalite\v5\schema",
            r".\altair\vegalite\v5\schema"
        ),
        (
            r"gm_dashboard_env\Lib\site-packages\streamlit\static",
            r".\streamlit\static"
        ),
        ('data/df_most_ten_frequent_prescreened_gm_year_model.csv', 'data'),
        ('gm_issues_dashboard.py', '.'),
        ('.streamlit/config.toml', '.streamlit')
    ] + copy_metadata('streamlit') + copy_metadata('pandas') + copy_metadata('matplotlib'),
    hiddenimports=[
        'streamlit', 
        'pandas',
        'streamlit.web.cli',
        'streamlit.runtime.scriptrunner.magic_funcs',
        'streamlit.runtime.caching.cache_data_api',
        'streamlit.runtime.legacy_caching',
        'importlib.metadata',
        'importlib_metadata'
    ],
    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data,
            cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run_gm_dashboard',
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
