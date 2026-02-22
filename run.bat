@echo off
REM Quick start script for Windows

echo ======================================
echo PDF Compliance Checker - Quick Start
echo ======================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Download from: https://www.python.org/
    exit /b 1
)

echo Step 1: Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Created venv
) else (
    echo venv already exists
)

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 4: Setting up project...
python setup.py

echo.
echo Step 5: Checking .env file...
if not exist ".env" (
    echo.
    echo ⚠️  .env file not found!
    echo Creating from template...
    copy .env.example .env
    echo Please edit .env and add your GOOGLE_API_KEY
    pause
)

echo.
echo Step 6: Starting Streamlit app...
streamlit run app.py

pause
