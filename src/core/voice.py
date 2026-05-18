import os
import subprocess
import shutil

class ChibiVoice:
    def __init__(self, engine="espeak"):
        self.engine = engine
        self.enabled = self._check_engine()

    def _check_engine(self):
        if self.engine == "espeak":
            return shutil.which("espeak") is not None
        return False

    def speak(self, text):
        print(f"CHIBI says: {text}")
        if not self.enabled:
            print("Voice output is disabled (engine not found).")
            return

        if self.engine == "espeak":
            try:
                # -v en-us+f3: US English, female voice variation 3
                # -s 160: speed 160 words per minute
                subprocess.run(["espeak", "-v", "en-us+f3", "-s", "160", text], check=True)
            except Exception as e:
                print(f"Voice output failed: {e}")
        elif self.engine == "piper":
            # Placeholder for Piper TTS integration
            pass

if __name__ == "__main__":
    voice = ChibiVoice()
    voice.speak("Hello! I am CHIBI, your autonomous desktop companion.")
