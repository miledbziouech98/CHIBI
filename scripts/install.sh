#!/bin/bash
echo "Setting up Yozu environment..."

# Detect CachyOS/Arch
if [ -f /etc/arch-release ]; then
    echo "Arch Linux / CachyOS detected. Ensuring system dependencies..."
    sudo pacman -S --needed python python-pip espeak-ng alsa-utils xdotool portaudio opencv
fi

# Check if ollama is installed
if ! command -v ollama &> /dev/null
then
    echo "Ollama could not be found. Please install it from https://ollama.com/"
    exit 1
fi

# Setup directory structure
mkdir -p assets
mkdir -p memory

# Pull Ollama models (Uncensored versions)
echo "Pulling Yozu's models..."
# Dolphin is a popular uncensored series. Llama 3.2 3B is lightweight.
ollama pull dolphin-llama3:8b-v2.9-q4_K_M # Reasoning (Uncensored)
ollama pull deepseek-coder:6.7b-instruct-q4_K_M # Coder (Better for 8GB than v2 Lite)
ollama pull llava:7b-v1.6-mistral-q4_K_M # Vision (Quantized)

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv || python -m venv venv

# OS-specific activation
if [ -d "venv/Scripts" ]; then
    echo "Activating Windows virtual environment..."
    source venv/Scripts/activate
else
    echo "Activating Linux/macOS virtual environment..."
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installation complete!"
