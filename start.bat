@echo off
REM Startup script for Mental Wellness Chatbot (Windows)
REM Usage: Double-click this file or run: start.bat

setlocal enabledelayedexpansion

echo 🌿 Mental Wellness Chatbot - Startup Script (Windows)
echo =====================================================

REM Check Python version
echo ✓ Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    echo    Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if venv exists
if not exist "venv" (
    echo ✓ Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate venv
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo ✓ Installing dependencies...
python -m pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo ⚠️  .env file not found!
    echo ✓ Creating .env from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env file and add your LLM configuration:
    echo    - HF_API_KEY for HuggingFace API, OR
    echo    - OLLAMA_URL for local Ollama setup
    echo.
    pause
)

REM Start the application
echo.
echo 🚀 Starting Mental Wellness Chatbot...
echo ====================================
echo.
echo Backend API: http://localhost:8000
echo Frontend: Open index.html in your browser
echo.
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

python main.py

pause
