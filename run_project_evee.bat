@echo off
title Project Evee - Voice Automation Assistant (DeepSeek GUI Version)
echo Starting Project Evee - DeepSeek GUI Version...
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
if not exist "base.py" (
    echo Error: base.py not found
    echo Please make sure you're running this from the Project Evee directory
    echo.
    pause
    exit /b 1
)

REM Check if DeepSeek module exists
if not exist "modules\deepseek_api_engine.py" (
    echo Error: DeepSeek API engine not found
    echo Please make sure all modules are installed
    echo.
    pause
    exit /b 1
)

REM Start the DeepSeek GUI application
echo Starting Project Evee with DeepSeek AI Engine and Windows GUI...
python base.py

REM If we get here, the application has closed
echo.
echo Project Evee (DeepSeek GUI Version) has closed.
echo.
echo Note: For the new terminal-based browser automation version, run:
echo   python main_gui.py
echo.
pause 