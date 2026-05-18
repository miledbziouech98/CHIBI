@echo off
echo Starting CHIBI...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Please run install.sh first.
    pause
    exit /b
)
python src/main.py
pause
