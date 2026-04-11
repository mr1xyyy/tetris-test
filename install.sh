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

# Install required packages
echo "Installing required Python packages..."
pip3 install windows-curses

echo "Installation complete!"

cd /tmp
git clone https://github.com/mr1xyyy/tetris-test.git 2>/dev/null || echo "Repository already exists in /tmp/tetris-test"
cd tetris-test

echo "Starting Tetris..."
python3 tetris.py