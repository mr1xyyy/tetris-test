#!/bin/bash
echo "Installing Tetris..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install it first."
    echo "On Ubuntu/Debian: sudo apt install python3"
    echo "On Fedora: sudo dnf install python3"
    echo "On Arch: sudo pacman -S python3"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    if command -v apt &> /dev/null; then
        sudo apt install -y python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-pip
    fi
fi

# Install required packages (curses is built-in on Linux, but check anyway)
echo "Checking curses module..."
python3 -c "import curses" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing windows-curses..."
    pip3 install windows-curses
fi

echo "All dependencies satisfied!"

# Clone and run
cd /tmp
git clone https://github.com/mr1xyyy/tetris-test.git 2>/dev/null || echo "Repository already exists in /tmp/tetris-test"
cd tetris-test

echo "Starting Tetris..."
python3 tetris.py