import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestInitialization(unittest.TestCase):
    def test_imports(self):
        try:
            from core.brain import YozuBrain
            from core.memory import YozuMemory
            from core.vision import YozuVision
            from core.action import YozuAction
            from ui.overlay import YozuOverlay
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_brain_init(self):
        from core.brain import YozuBrain
        brain = YozuBrain()
        self.assertEqual(brain.reasoning_model, "dolphin-llama3:8b-v2.9-q4_K_M")

    def test_memory_init(self):
        from core.memory import YozuMemory
        # Use a temporary memory path for testing
        memory = YozuMemory(memory_path="tests/test_memory")
        self.assertTrue(os.path.exists("tests/test_memory"))

if __name__ == "__main__":
    unittest.main()
