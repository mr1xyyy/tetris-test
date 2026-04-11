@echo off
echo Installing Tetris...

REM Check if Python is installed
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python 3 is not installed.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found:
py -3 --version

REM Download tetris.py if not present
if not exist tetris.py (
    echo Downloading tetris.py...
    curl -LO https://raw.githubusercontent.com/mr1xyyy/tetris-test/main/tetris.py
    if errorlevel 1 (
        echo Error: Failed to download tetris.py
        pause
        exit /b 1
    )
)

REM Install required packages
echo Installing required Python packages...
py -3 -m pip install windows-curses

echo Installation complete!
echo Starting Tetris...
py -3 tetris.py

pause
