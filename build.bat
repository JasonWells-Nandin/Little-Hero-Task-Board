@echo off
chcp 65001 >nul
echo Building application as executable...
echo.

python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

python build_exe.py

echo.
echo Build complete! Check the dist directory.
pause
