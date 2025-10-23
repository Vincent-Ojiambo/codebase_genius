#!/bin/bash

# Codebase Genius - Production Deployment Script
# This script demonstrates how to deploy and run the system

echo "🚀 Codebase Genius - Production Deployment"
echo "=========================================="

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v jac &> /dev/null; then
    echo "❌ Jac is not installed. Installing..."
    pip install jaclang
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Jac. Please install manually:"
        echo "   pip install jaclang"
        exit 1
    fi
fi

echo "✅ Jac found: $(jac --version)"

if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git."
    exit 1
fi

echo "✅ Git found: $(git --version)"

# Setup virtual environment
echo "📦 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p outputs
mkdir -p logs

# Set permissions
chmod +x setup.sh

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "To start the system:"
echo "1. Activate environment: source venv/bin/activate"
echo "2. Start server: jac serve main.jac"
echo "3. Test API: curl http://localhost:8000/walker/api/get_status"
echo ""
echo "Example usage:"
echo 'curl -X POST http://localhost:8000/walker/api/generate_docs \'
echo '  -H "Content-Type: application/json" \'
echo '  -d "{\"repo_url\": \"https://github.com/octocat/Hello-World\"}"'
echo ""
echo "📖 See README.md for detailed instructions"
