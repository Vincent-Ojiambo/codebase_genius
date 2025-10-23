#!/bin/bash

# Codebase Genius Setup Script
# This script sets up the development environment for the Codebase Genius system

echo "🤖 Codebase Genius Setup Script"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git."
    exit 1
fi

echo "✅ Git found: $(git --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "✅ Virtual environment ready"

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create output directory
echo "📁 Creating output directories..."
mkdir -p outputs
mkdir -p logs

# Set permissions
chmod +x test_system.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the system:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Start the Jac server: jac serve main.jac"
echo "3. Open browser to: http://localhost:8000"
echo "4. Or run the web interface: python3 -m http.server 3000 (in the project root)"
echo ""
echo "To test the system:"
echo "python3 test_system.py"
echo ""
echo "To generate documentation for a sample repository:"
echo 'curl -X POST http://localhost:8000/walker/api/generate_docs -H "Content-Type: application/json" -d "{\"repo_url\": \"https://github.com/octocat/Hello-World\"}"'
