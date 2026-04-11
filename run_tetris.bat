@echo off
echo Installing Tetris...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Install required packages
echo Installing required Python packages...
py -3 -m pip install windows-curses

echo Installation complete!
echo Starting Tetris...
python tetris.py

pause
