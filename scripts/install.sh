#!/bin/bash
echo "Setting up CHIBI environment..."

# Check if ollama is installed
if ! command -v ollama &> /dev/null
then
    echo "Ollama could not be found. Please install it from https://ollama.com/"
    exit 1
fi

# Setup bin directory
mkdir -p bin/piper
mkdir -p assets

# Download Piper TTS if not present
if [ ! -f "bin/piper/piper" ]; then
    echo "Downloading Piper TTS engine..."
    # Using a stable release URL for Linux x86_64
    curl -L https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz -o bin/piper.tar.gz
    tar -xzf bin/piper.tar.gz -C bin/piper --strip-components=1
    rm bin/piper.tar.gz
fi

# Download a high-quality female voice model for "Chibi" sound
if [ ! -f "assets/voice_model.onnx" ]; then
    echo "Downloading Chibi voice model..."
    # Using a high-quality en_US female model
    curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx -o assets/voice_model.onnx
    curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json -o assets/voice_model.onnx.json
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

# Check for audio player
if ! command -v aplay &> /dev/null
then
    echo "Warning: 'aplay' not found. Voice playback might fail."
    echo "Install with: sudo apt-get install alsa-utils"
fi

echo "Installation complete!"
