import pyautogui

class ChibiAction:
    def __init__(self):
        pyautogui.FAILSAFE = True

    def click(self, x, y):
        pyautogui.click(x, y)

    def type_text(self, text):
        pyautogui.write(text, interval=0.1)

    def press_key(self, key):
        pyautogui.press(key)

    def hotkey(self, *args):
        pyautogui.hotkey(*args)
