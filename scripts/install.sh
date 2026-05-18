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

# Download Piper TTS if not present (Linux only for now in script)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ ! -f "bin/piper/piper" ]; then
        echo "Downloading Piper TTS engine (Linux)..."
        curl -L https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz -o bin/piper.tar.gz
        tar -xzf bin/piper.tar.gz -C bin/piper --strip-components=1
        rm bin/piper.tar.gz
    fi
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    echo "Windows detected. Piper TTS binary download skipped (please download manually if needed or use espeak)."
fi

# Download a high-quality female voice model
if [ ! -f "assets/voice_model.onnx" ]; then
    echo "Downloading Chibi voice model..."
    curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx -o assets/voice_model.onnx
    curl -L https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json -o assets/voice_model.onnx.json
fi

# Pull Ollama models
echo "Pulling Ollama models..."
ollama pull qwen:4b
ollama pull codellama:7b

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
