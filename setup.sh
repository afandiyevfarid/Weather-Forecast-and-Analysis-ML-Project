#!/bin/bash

# Advanced Weather Analytics Dashboard - Setup Script

echo "🌍 Advanced Weather Analytics Dashboard - Setup"
echo "=============================================="

# Check Python version
echo -e "\n📍 Checking Python installation..."
python3 --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install Python first."
    exit 1
fi

echo "✅ Python and pip3 are available"

# Create virtual environment
echo -e "\n📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo -e "\n⬇️  Installing dependencies..."
pip install -r requirements.txt

echo -e "\n✅ Installation complete!"
echo -e "\n🚀 To start the dashboard, run:"
echo "   source venv/bin/activate"
echo "   streamlit run finalprj.py"
echo -e "\n📊 The dashboard will open at http://localhost:8501"
