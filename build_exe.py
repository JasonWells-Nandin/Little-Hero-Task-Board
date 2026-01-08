import PyInstaller.__main__
import os
import shutil
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = Path(__file__).parent
ICON_ICO = ROOT / "task_icon_tmp.ico"

for p in ["build", "dist", "task_manager.spec", ICON_ICO]:
    if os.path.exists(p):
        if os.path.isdir(p):
            shutil.rmtree(p)
        else:
            os.remove(p)

icon_arg = "--icon=NONE"

args = [
    'task_manager.py',
    '--name=TaskManager',
    '--onefile',
    '--windowed',
    icon_arg,
    '--clean',
    '--noconfirm'
]

if os.path.exists('task_data.json'):
    args.insert(-2, '--add-data=task_data.json;.')

PyInstaller.__main__.run(args)

if ICON_ICO.exists():
    ICON_ICO.unlink()

print("\nBuild complete! Executable is in the dist directory.")
