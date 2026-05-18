#!/bin/bash
echo "Setting up CHIBI environment..."

# Check if ollama is installed
if ! command -v ollama &> /dev/null
then
    echo "Ollama could not be found. Please install it from https://ollama.com/"
    exit 1
fi

# Check for espeak (used for TTS)
if ! command -v espeak &> /dev/null
then
    echo "Warning: espeak not found. TTS will be disabled."
    echo "You can install it with: sudo apt-get install espeak (on Debian/Ubuntu)"
fi

# Pull Ollama models
echo "Pulling Ollama models..."
ollama pull qwen:4b
ollama pull codellama:7b

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation complete!"
