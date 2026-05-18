import sys
import threading
import time
from PyQt6.QtWidgets import QApplication
from ui.overlay import ChibiOverlay
from core.brain import ChibiBrain
from core.memory import ChibiMemory
from core.vision import ChibiVision
from core.action import ChibiAction
from core.voice import ChibiVoice

class ChibiApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.overlay = ChibiOverlay()
        self.brain = ChibiBrain()
        self.memory = ChibiMemory()
        self.vision = ChibiVision()
        self.action = ChibiAction()
        self.voice = ChibiVoice()

        self.is_running = True
        self.thought_thread = threading.Thread(target=self.reasoning_loop, daemon=True)

    def reasoning_loop(self):
        print("Starting recursive reasoning loop...")
        while self.is_running:
            try:
                # 1. Environmental Awareness
                active_window = self.vision.get_active_window()

                # 2. Reasoning Loop
                prompt = f"I am observing the desktop. The active window is '{active_window}'. What should I reflect on or do right now? Keep it brief."
                thought = self.brain.query(prompt)

                # 3. Memory Persistence
                self.memory.save_thought("Daily Reflection", thought, tags=["reflection", "environment"])

                # 4. Action & Body Update
                print(f"Thought: {thought}")
                # For now, just blink or look like thinking
                self.overlay.renderer.set_state("talking")
                # self.voice.speak(thought) # Optional: only speak if important
                time.sleep(2)
                self.overlay.renderer.set_state("idle")

                # Wait before next cycle to save resources (important for 8GB RAM)
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
