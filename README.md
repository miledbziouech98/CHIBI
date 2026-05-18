# CHIBI - Autonomous Desktop Companion AI

CHIBI is a lightweight, autonomous desktop companion AI designed for local execution. It features a chibi anime aesthetic and a "Second Brain" memory system integrated with Obsidian.

## Features
- **Modular Cognition:** Uses Qwen 4B for reasoning and Code Llama 7B for coding.
- **Persistent Memory:** Stores thoughts and goals in Markdown files (Obsidian compatible) and uses ChromaDB for semantic retrieval.
- **Desktop Awareness:** Tracks active windows and can interact with the desktop using PyAutoGUI.
- **Transparent UI:** A PyQt6-based overlay that sits on top of your desktop.
- **High-Quality Voice:** Integrated Piper TTS with a friendly female voice, optimized for a "chibi" feel.

## Prerequisites
- [Ollama](https://ollama.com/) (Must be installed and running)
- System dependencies for audio and UI (Linux):
  ```bash
  sudo apt-get install espeak alsa-utils libxcb-cursor0
  ```

## Installation
1. Run the installation script:
   ```bash
   bash scripts/install.sh
   ```
   *This will pull models and download the Piper TTS engine (approx. 200MB).*

## Usage
Start CHIBI by running:
```bash
bash scripts/start.sh
```

## Project Structure
- `src/`: Source code
  - `ui/`: PyQt6 overlay and rendering
  - `core/`: Brain, Memory, Vision, Action, and Voice modules
- `assets/`: Visual assets (SVG, images) and voice models
- `memory/`: Obsidian-compatible memory vault
- `scripts/`: Install and start scripts
- `bin/`: Local binaries (Piper TTS)
