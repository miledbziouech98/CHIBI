import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QPoint
from ui.renderer import YozuRenderer

class YozuOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window flags for transparency, stay-on-top, and click-through
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add image renderer
        self.renderer = YozuRenderer()
        self.layout.addWidget(self.renderer)

        # Set window size to match content (300x300)
        self.setFixedSize(300, 300)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = YozuOverlay()
    overlay.show()
    sys.exit(app.exec())
