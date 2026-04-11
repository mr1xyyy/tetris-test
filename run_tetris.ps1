Write-Host "Installing Tetris..." -ForegroundColor Cyan

# Check if Python 3 is installed
$pythonCmd = $null
$pyVersions = @("py", "python", "python3")
foreach ($cmd in $pyVersions) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $version = & $cmd --version 2>&1
        if ($version -match "Python 3") {
            $pythonCmd = $cmd
            break
        }
    }
}

if (-not $pythonCmd) {
    Write-Host "Error: Python 3 is not installed." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python found: " -NoNewline
& $pythonCmd --version

# Download tetris.py if not present
if (-not (Test-Path "tetris.py")) {
    Write-Host "Downloading tetris.py..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/mr1xyyy/tetris-test/main/tetris.py" -OutFile "tetris.py"
    } catch {
        Write-Host "Error: Failed to download tetris.py" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Install required packages
Write-Host "Installing required Python packages..." -ForegroundColor Cyan
& $pythonCmd -m pip install windows-curses

Write-Host "Installation complete!" -ForegroundColor Green
Write-Host "Starting Tetris..." -ForegroundColor Green
& $pythonCmd tetris.py
