import sys
import threading
import time
import asyncio
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from ui.overlay import YozuOverlay
from core.brain import YozuBrain
from core.memory import YozuMemory
from core.vision import YozuVision
from core.action import YozuAction
from core.voice import YozuVoice
from core.telegram_bot import YozuTelegramBot
from core.mcp_server import YozuMCP
from core.n8n_client import Yozun8n
from core.media import YozuMediaGenerator

class YozuSignals(QObject):
    update_state = pyqtSignal(str)

class YozuApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.overlay = YozuOverlay()
        self.brain = YozuBrain()
        self.memory = YozuMemory()
        self.vision = YozuVision()
        self.action = YozuAction()
        self.voice = YozuVoice()
        self.mcp = YozuMCP()
        self.n8n = Yozun8n()
        self.media = YozuMediaGenerator()
        self.telegram = YozuTelegramBot(self.brain, self.memory, voice_callback=self.voice.speak)

        self.signals = YozuSignals()
        self.signals.update_state.connect(self.overlay.renderer.set_state)

        self.is_running = True
        self.thought_thread = threading.Thread(target=self.reasoning_loop, daemon=True)
        self.telegram_thread = threading.Thread(target=self.start_telegram, daemon=True)

    def start_telegram(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.telegram.start())
        loop.run_forever()

    def reasoning_loop(self):
        print("Starting recursive reasoning loop...")
        while self.is_running:
            try:
                # 1. Environmental Awareness
                active_window = self.vision.get_active_window()

                # 2. Memory Retrieval (Contextual awareness)
                past_context = ""
                relevant_memories = self.memory.retrieve_relevant(f"Activity in {active_window}")
                if relevant_memories and 'documents' in relevant_memories:
                    past_context = "\n".join(relevant_memories['documents'][0])

                # 3. Reasoning Loop
                prompt = f"I am Yozu, observing the desktop. The active window is '{active_window}'."
                if past_context:
                    prompt += f"\nRelevant past thoughts:\n{past_context}"
                prompt += "\nWhat should I, Yozu, reflect on or do right now? Keep it brief."

                # Combine all tool definitions
                all_tools = self.mcp.get_tool_definitions() + self.n8n.get_tool_definitions()
                self.tool_instances = {'mcp': self.mcp, 'n8n': self.n8n}

                thought = self.brain.query(prompt, tools=all_tools, tool_instances=self.tool_instances)
                # If thought indicates tool intent, handle it (query method now handles this internally if configured)

                # 4. Memory Persistence
                self.memory.save_thought("Yozu Reflection", thought, tags=["reflection", "environment", active_window])

                # 5. Action & Body Update
                print(f"Thought: {thought}")

                # Use signal to update UI state safely
                self.signals.update_state.emit("talking")
                self.voice.speak(thought)
                time.sleep(2)
                self.signals.update_state.emit("idle")

                # Wait before next cycle
                time.sleep(30)
            except Exception as e:
                print(f"Error in reasoning loop: {e}")
                time.sleep(10)

    def run(self):
        self.overlay.show()
        self.thought_thread.start()
        self.telegram_thread.start()
        print("Yozu is now active!")
        sys.exit(self.app.exec())

if __name__ == "__main__":
    yozu = YozuApp()
    yozu.run()
