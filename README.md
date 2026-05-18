# CHIBI - Autonomous Desktop Companion AI

CHIBI is a lightweight, autonomous desktop companion AI designed for local execution. It features a chibi anime aesthetic and a "Second Brain" memory system integrated with Obsidian.

## Features
- **Modular Cognition:** Uses Qwen 3.5 4B for reasoning and Code Llama 7B for coding.
- **Persistent Memory:** Stores thoughts and goals in Markdown files (Obsidian compatible) and uses ChromaDB for semantic retrieval.
- **Desktop Awareness:** Tracks active windows and can interact with the desktop using PyAutoGUI.
- **Transparent UI:** A PyQt6-based overlay that sits on top of your desktop.

## Installation
1. Ensure [Ollama](https://ollama.com/) is installed and running.
2. Run the installation script:
   ```bash
   bash scripts/install.sh
   ```

## Usage
Start CHIBI by running:
```bash
bash scripts/start.sh
```

## Project Structure
- `src/`: Source code
  - `ui/`: PyQt6 overlay and rendering
  - `core/`: Brain, Memory, Vision, and Action modules
- `assets/`: Visual assets (SVG, images)
- `memory/`: Obsidian-compatible memory vault
- `scripts/`: Install and start scripts
