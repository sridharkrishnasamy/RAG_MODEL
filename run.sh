#!/bin/bash

# Quick start script for Linux/macOS

echo "======================================"
echo "PDF Compliance Checker - Quick Start"
echo "======================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Error: Python3 is not installed"
    echo "Install from: https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"

echo ""
echo "Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Created venv"
else
    echo "✓ venv already exists"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Activated"

echo ""
echo "Step 3: Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "Step 4: Setting up project..."
python setup.py

echo ""
echo "Step 5: Checking .env file..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo "Please edit .env and add your GOOGLE_API_KEY"
    echo "Press Enter to continue..."
    read
else
    echo "✓ .env file found"
fi

echo ""
echo "Step 6: Starting Streamlit app..."
echo "Opening http://localhost:8501 in your browser..."
echo ""

streamlit run app.py
