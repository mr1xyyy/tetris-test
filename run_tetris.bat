@echo off
echo Installing Tetris...

REM Detect available Python 3 versions using py launcher
set PYTHON=

for /f "tokens=2 delims=- " %%v in ('py --list 2^>nul ^| findstr /r "^ *-3\." ^| sort /r') do (
    set PYTHON=py -%%v
    goto :found
)

REM Fallback: try py -3
py -3 --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON=py -3
) else (
    echo Error: Python 3 is not installed.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:found
echo Python found:
%PYTHON% --version

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
%PYTHON% -m pip install windows-curses

echo Installation complete!
echo Starting Tetris...
%PYTHON% tetris.py

pause
