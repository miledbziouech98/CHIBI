import sys
import threading
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from ui.overlay import ChibiOverlay
from core.brain import ChibiBrain
from core.memory import ChibiMemory
from core.vision import ChibiVision
from core.action import ChibiAction
from core.voice import ChibiVoice

class ChibiSignals(QObject):
    update_state = pyqtSignal(str)

class ChibiApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.overlay = ChibiOverlay()
        self.brain = ChibiBrain()
        self.memory = ChibiMemory()
        self.vision = ChibiVision()
        self.action = ChibiAction()
        self.voice = ChibiVoice()

        self.signals = ChibiSignals()
        self.signals.update_state.connect(self.overlay.renderer.set_state)

        self.is_running = True
        self.thought_thread = threading.Thread(target=self.reasoning_loop, daemon=True)

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
                prompt = f"I am observing the desktop. The active window is '{active_window}'."
                if past_context:
                    prompt += f"\nRelevant past thoughts:\n{past_context}"
                prompt += "\nWhat should I reflect on or do right now? Keep it brief."

                thought = self.brain.query(prompt)

                # 4. Memory Persistence
                self.memory.save_thought("Daily Reflection", thought, tags=["reflection", "environment", active_window])

                # 5. Action & Body Update
                print(f"Thought: {thought}")

                # Use signal to update UI state safely
                self.signals.update_state.emit("talking")
                # self.voice.speak(thought)
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
        print("CHIBI is now active!")
        sys.exit(self.app.exec())

if __name__ == "__main__":
    chibi = ChibiApp()
    chibi.run()
