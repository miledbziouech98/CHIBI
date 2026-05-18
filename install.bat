@echo off
setlocal enabledelayedexpansion
echo Setting up CHIBI environment for Windows...

:: Check for Python and avoid the "App Installer" trap
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found!
    echo If the Microsoft Store opened, please:
    echo 1. Search for "App execution aliases" in Windows.
    echo 2. Turn OFF "python.exe" and "python3.exe".
    echo 3. Install Python from https://www.python.org/
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

:: Create directories
if not exist assets mkdir assets
if not exist bin\piper mkdir bin\piper

:: Download Piper TTS Binary for Windows
if not exist bin\piper\piper.exe (
    echo Downloading Piper TTS engine (Windows)...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_windows_amd64.zip' -OutFile 'bin\piper.zip'"
    echo Extracting Piper...
    powershell -Command "Expand-Archive -Path 'bin\piper.zip' -DestinationPath 'bin\piper_temp' -Force"
    move bin\piper_temp\piper\* bin\piper\
    rmdir /s /q bin\piper_temp
    del bin\piper.zip
)

:: Download voice model
if not exist assets\voice_model.onnx (
    echo Downloading voice model...
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx' -OutFile 'assets\voice_model.onnx'"
    powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/en_US-amy-medium.onnx.json' -OutFile 'assets\voice_model.onnx.json'"
)

:: Pull Ollama models
echo Pulling Ollama models...
ollama pull qwen:4b
ollama pull codellama:7b

:: Create virtual environment
echo Creating virtual environment...
if exist venv (
    if not exist venv\Scripts\activate.bat (
        rmdir /s /q venv
    )
)

python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment.
    echo Try running this script as Administrator.
    pause
    exit /b
)

:: Activate and install requirements
echo Installing dependencies...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation complete!
echo You can now start CHIBI by double-clicking 'start.bat'
pause
