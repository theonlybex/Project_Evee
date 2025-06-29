@echo off
title Project Evee - Voice Automation Assistant
echo Starting Project Evee...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "main_gui.py" (
    echo Error: main_gui.py not found
    echo Please make sure you're running this from the Project Evee directory
    echo.
    pause
    exit /b 1
)

REM Start the application
python main_gui.py

REM If we get here, the application has closed
echo.
echo Project Evee has closed.
pause 