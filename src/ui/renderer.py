import os
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import Qt, QTimer

class ChibiRenderer(QSvgWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.svg_path = os.path.join(os.path.dirname(__file__), "../../assets/chibi.svg")
        self.load(self.svg_path)
        self.state = "idle"

        # Original SVG content for manipulation
        with open(self.svg_path, 'r') as f:
            self.base_svg = f.read()

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500) # Check state every 500ms

        self.blink_count = 0

    def set_state(self, state):
        self.state = state
        self.apply_state()

    def apply_state(self):
        modified_svg = self.base_svg

        # Handle blinking (simplified manipulation)
        if self.state == "blinking":
            modified_svg = modified_svg.replace('id="eye_left"', 'id="eye_left" style="display: none;"')
            modified_svg = modified_svg.replace('id="eye_right"', 'id="eye_right" style="display: none;"')
            modified_svg = modified_svg.replace('id="eyes_closed" style="display: none;"', 'id="eyes_closed"')

        # Handle talking
        if self.state == "talking":
            modified_svg = modified_svg.replace('id="mouth_idle"', 'id="mouth_idle" style="display: none;"')
            modified_svg = modified_svg.replace('id="mouth_talk" fill="#a00" cx="150" cy="165" r="5" style="display: none;"', 'id="mouth_talk" fill="#a00" cx="150" cy="165" r="5"')

        self.load(modified_svg.encode('utf-8'))

    def update_animation(self):
        # Idle animation: random blinks
        import random
        if self.state == "idle":
            if random.random() < 0.1:
                self.set_state("blinking")
                QTimer.singleShot(150, lambda: self.set_state("idle"))

        # If talking, maybe pulse the mouth?
        # (This is a placeholder for more complex animation logic)
        pass
