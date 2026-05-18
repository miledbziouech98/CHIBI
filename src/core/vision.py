import pyautogui
import cv2
import numpy as np
import subprocess
import shutil

try:
    import pygetwindow as gw
    HAS_GW = True
except (ImportError, NotImplementedError):
    HAS_GW = False

class ChibiVision:
    def __init__(self):
        self.has_xdotool = shutil.which("xdotool") is not None

    def get_active_window(self):
        if HAS_GW:
            try:
                win = gw.getActiveWindow()
                return win.title if win else "Desktop"
            except:
                pass

        if self.has_xdotool:
            try:
                # Get the active window ID and then its name
                window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
                window_name = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode().strip()
                return window_name
            except:
                return "Desktop (xdotool failed)"

        return "Active Window (Generic Fallback)"

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
