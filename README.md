# CHIBI - Autonomous Desktop Companion AI

CHIBI is a lightweight, autonomous desktop companion AI designed for local execution. It features a chibi anime aesthetic and a "Second Brain" memory system integrated with Obsidian.

## Features
- **Modular Cognition:** Uses Qwen 4B for reasoning and Code Llama 7B for coding.
- **Persistent Memory:** Stores thoughts and goals in Markdown files (Obsidian compatible) and uses ChromaDB for semantic retrieval.
- **Desktop Awareness:** Tracks active windows and can interact with the desktop using PyAutoGUI.
- **Transparent UI:** A PyQt6-based overlay that sits on top of your desktop.
- **High-Quality Voice:** Integrated Piper TTS with a friendly female voice.

## Prerequisites
- [Ollama](https://ollama.com/) (Must be installed and running)
- System dependencies (Linux): `sudo apt-get install espeak alsa-utils libxcb-cursor0 xdotool`

## Installation

### Windows (Recommended)
1. Double-click **`install.bat`** in the root folder.
2. If it fails with "Permission Denied", right-click it and select **"Run as Administrator"**.

### Linux / Git Bash
1. Run: `bash scripts/install.sh`

## Usage
- **Windows:** Double-click **`start.bat`**.
- **Linux:** Run `bash scripts/start.sh`.

## Troubleshooting (Windows)
- **"Microsoft Store opens" or "Python not found":**
  1. Open Windows Start menu and type **"App execution aliases"**.
  2. Find **"python.exe"** and **"python3.exe"** and turn them **OFF**.
  3. Re-run `install.bat`.
- **"Permission Denied" in Git Bash:**
  Git Bash sometimes has issues with file permissions. We highly recommend using **`install.bat`** in a standard Command Prompt or PowerShell as Administrator for the best experience.
- **"venv/bin/activate: No such file":**
  This happens when running the Linux script on Windows. Always use `.bat` files on Windows.

## Project Structure
- `src/`: Source code
- `assets/`: Character design (SVG) and Voice models
- `memory/`: Obsidian vault
- `scripts/`: Platform-specific scripts
