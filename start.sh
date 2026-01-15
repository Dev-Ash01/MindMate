#!/bin/bash
# Startup script for Mental Wellness Chatbot
# Usage: ./start.sh

set -e

echo "🌿 Mental Wellness Chatbot - Startup Script"
echo "==========================================="

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "✓ Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install requirements
echo "✓ Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "✓ Creating .env from template..."
    cp .env.example .env
    echo "  ⚠️  IMPORTANT: Edit .env and add your LLM configuration:"
    echo "     - HF_API_KEY for HuggingFace API, OR"
    echo "     - OLLAMA_URL for local Ollama setup"
fi

# Start the application
echo ""
echo "🚀 Starting Mental Wellness Chatbot..."
echo "==========================================="
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend: Open index.html in your browser"
echo ""
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python main.py
