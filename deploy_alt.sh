#!/bin/bash

# Codebase Genius - Alternative Deployment Script
# This script provides multiple deployment options if Railway fails

echo "🚀 Codebase Genius - Alternative Deployment Options"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "main.jac" ] && [ ! -d "codebase_genius" ]; then
    echo "❌ Error: Please run this script from the repository root"
    exit 1
fi

echo "📦 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Creating directories..."
mkdir -p outputs logs

echo ""
echo "✅ Setup complete! Choose deployment option:"
echo ""
echo "1️⃣  Local Development (Recommended)"
echo "   jac serve main.jac"
echo "   Access: http://localhost:8000"
echo ""
echo "2️⃣  Docker Deployment"
echo "   docker build -t codebase-genius ."
echo "   docker run -p 8000:8000 codebase-genius"
echo "   Access: http://localhost:8000"
echo ""
echo "3️⃣  Docker Compose (with web interface)"
echo "   docker-compose up -d"
echo "   Access: http://localhost:8000 (API), http://localhost:3000 (Web)"
echo ""
echo "4️⃣  Railway Manual Deployment"
echo "   - Go to railway.app"
echo "   - Create new project"
echo "   - Connect this GitHub repository"
echo "   - Deploy automatically"
echo ""
echo "5️⃣  Heroku Deployment"
echo "   # Install Heroku CLI first"
echo "   heroku create codebase-genius-$(date +%s)"
echo "   git push heroku master"
echo ""
echo "🧪 Test the deployment:"
echo "curl -X POST http://localhost:8000/walker/api/generate_docs \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"repo_url\": \"https://github.com/octocat/Hello-World\"}'"
echo ""
echo "📖 Web interface: Open http://localhost:3000 in your browser"
echo ""
echo "🎉 Happy documenting!"
