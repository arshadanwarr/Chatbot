#!/bin/bash

# Chatbot Setup Script
# This script helps you set up the AI Chatbot with LangChain and Ollama

set -e

echo "=================================="
echo "AI Chatbot Setup Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Check if Python is installed
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python is installed: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Ollama is installed
print_info "Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    print_success "Ollama is installed"
else
    print_error "Ollama is not installed."
    echo ""
    echo "Please install Ollama from https://ollama.ai"
    echo ""
    echo "Installation commands:"
    echo "  macOS/Linux: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "  Or download from: https://ollama.ai/download"
    exit 1
fi

# Create virtual environment
print_info "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"

# Create .env file if it doesn't exist
print_info "Setting up environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Created .env file from .env.example"
else
    print_success ".env file already exists"
fi

# Check if Ollama is running
print_info "Checking if Ollama service is running..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_success "Ollama is running"
else
    print_error "Ollama is not running. Starting Ollama..."
    echo ""
    echo "Please run in a separate terminal:"
    echo "  ollama serve"
    echo ""
fi

# Pull default model
print_info "Checking for llama2 model..."
if ollama list | grep -q "llama2"; then
    print_success "llama2 model is already installed"
else
    echo ""
    read -p "Would you like to pull the llama2 model now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Pulling llama2 model (this may take a while)..."
        ollama pull llama2
        print_success "llama2 model installed"
    else
        print_info "Skipping model installation. You can pull it later with: ollama pull llama2"
    fi
fi

echo ""
echo "=================================="
print_success "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Make sure Ollama is running:"
echo "   ollama serve"
echo ""
echo "2. Activate the virtual environment (if not already activated):"
echo "   source venv/bin/activate"
echo ""
echo "3. Start the chatbot API:"
echo "   python main.py"
echo ""
echo "4. Test the chatbot:"
echo "   python client.py"
echo ""
echo "5. Or open frontend.html in your browser"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "=================================="
echo ""