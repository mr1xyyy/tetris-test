@echo off
chcp 65001 > nul
cd /d "%~dp0"

py -3 tetris_terminal.py --delay 0.4

pause
