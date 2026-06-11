#!/bin/bash
echo "Starting Yozu..."

# OS-specific activation
if [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Run the application
python3 src/main.py || python src/main.py
