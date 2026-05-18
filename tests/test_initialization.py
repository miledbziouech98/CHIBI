import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestInitialization(unittest.TestCase):
    def test_imports(self):
        try:
            from core.brain import ChibiBrain
            from core.memory import ChibiMemory
            from core.vision import ChibiVision
            from core.action import ChibiAction
            from ui.overlay import ChibiOverlay
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_brain_init(self):
        from core.brain import ChibiBrain
        brain = ChibiBrain()
        self.assertEqual(brain.reasoning_model, "qwen3.5:4b")

    def test_memory_init(self):
        from core.memory import ChibiMemory
        # Use a temporary memory path for testing if possible,
        # but here we just check if it initializes.
        memory = ChibiMemory(memory_path="tests/test_memory")
        self.assertTrue(os.path.exists("tests/test_memory"))

if __name__ == "__main__":
    unittest.main()
