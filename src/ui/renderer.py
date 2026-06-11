import os
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer

class YozuRenderer(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = os.path.join(os.path.dirname(__file__), "../../assets/yozu.png")
        self.pixmap = QPixmap(self.image_path)
        self.setPixmap(self.pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.state = "idle"

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(500) # Check state every 500ms

    def set_state(self, state):
        self.state = state
        self.apply_state()

    def apply_state(self):
        # For now, we just have a static image.
        # Future: swap between different PNGs for blinking/talking
        pass

    def update_animation(self):
        pass
