import pyautogui
import cv2
import numpy as np

try:
    import pygetwindow as gw
    HAS_GW = True
except (ImportError, NotImplementedError):
    HAS_GW = False

class ChibiVision:
    def __init__(self):
        pass

    def get_active_window(self):
        if HAS_GW:
            try:
                return gw.getActiveWindow().title
            except:
                return "Unknown"
        else:
            # Fallback for Linux or when pygetwindow is unavailable
            return "Active Window (Linux Fallback)"

    def take_screenshot(self):
        try:
            screenshot = pyautogui.screenshot()
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Screenshot failed: {e}")
            return np.zeros((100, 100, 3), dtype=np.uint8)

    def find_on_screen(self, template_path):
        screen = self.take_screenshot()
        template = cv2.imread(template_path)
        if template is None:
            return []
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        return list(zip(*loc[::-1]))
