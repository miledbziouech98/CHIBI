@echo off
echo Setting up CHIBI environment for Windows...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python from python.org
    pause
    exit /b
)

:: Check for Ollama
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama not found. Please install it from ollama.com and make sure it is running.
    pause
    exit /b
)

:: Create assets directory
if not exist assets mkdir assets

:: Download voice model
if not exist assets\voice_model.onnx (
    echo Downloading voice model...
    powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx' -OutFile 'assets\voice_model.onnx'"
    powershell -Command "Invoke-WebRequest -Uri 'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json' -OutFile 'assets\voice_model.onnx.json'"
)

:: Pull Ollama models
echo Pulling Ollama models...
ollama pull qwen:4b
ollama pull codellama:7b

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate and install requirements
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo Installation complete!
pause
