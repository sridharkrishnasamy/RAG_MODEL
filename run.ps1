# Quick start script for PowerShell (Windows)

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "PDF Compliance Checker - Quick Start" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 1: Creating virtual environment..." -ForegroundColor Yellow
if (!(Test-Path "venv")) {
    python -m venv venv
    Write-Host "✓ Created venv" -ForegroundColor Green
} else {
    Write-Host "✓ venv already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Activated" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Setting up project..." -ForegroundColor Yellow
python setup.py

Write-Host ""
Write-Host "Step 5: Checking .env file..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host "Please edit .env and add your GOOGLE_API_KEY" -ForegroundColor Yellow
    pause
} else {
    Write-Host "✓ .env file found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 6: Starting Streamlit app..." -ForegroundColor Yellow
Write-Host "Opening http://localhost:8501 in your browser..." -ForegroundColor Cyan
Write-Host ""

streamlit run app.py
