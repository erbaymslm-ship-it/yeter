@echo off
REM Setup script for Windows development
REM This allows you to test the Kivy app on Windows
echo Setting up Elixir Technology project for Windows...

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

REM Install required packages
echo.
echo Installing required packages...
pip install kivy==2.3.0 kivymd==1.2.0 pillow numpy

echo.
echo Setup complete! You can now run:
echo   python main.py
echo.
pause
