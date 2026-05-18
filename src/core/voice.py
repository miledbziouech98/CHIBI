import os
import subprocess
import shutil

class ChibiVoice:
    def __init__(self, engine="piper"):
        self.engine = engine
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
        self.piper_path = os.path.join(self.base_dir, "bin/piper/piper")
        self.model_path = os.path.join(self.base_dir, "assets/voice_model.onnx")
        self.config_path = self.model_path + ".json"

        self.enabled = self._check_engine()

    def _check_engine(self):
        if self.engine == "piper":
            return os.path.exists(self.piper_path) and os.path.exists(self.model_path)
        elif self.engine == "espeak":
            return shutil.which("espeak") is not None
        return False

    def speak(self, text):
        print(f"CHIBI says: {text}")
        if not self.enabled:
            print(f"Voice output is disabled ({self.engine} engine or model not found).")
            return

        if self.engine == "piper":
            try:
                # Piper takes text from stdin and outputs raw audio to stdout,
                # which we then pipe to an audio player like 'aplay' or 'paplay'.
                # We use a high pitch/speed to make it sound more 'chibi'.
                piper_process = subprocess.Popen(
                    [self.piper_path, "--model", self.model_path, "--output_raw"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL
                )

                # Use 'aplay' (common on Linux) to play the raw audio
                # Piper medium models are usually 22050Hz
                aplay_process = subprocess.Popen(
                    ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw"],
                    stdin=piper_process.stdout
                )

                piper_process.stdin.write(text.encode('utf-8'))
                piper_process.stdin.close()
                aplay_process.wait()

            except Exception as e:
                print(f"Piper Voice output failed: {e}")

        elif self.engine == "espeak":
            try:
                subprocess.run(["espeak", "-v", "en-us+f3", "-s", "170", "-p", "80", text], check=True)
            except Exception as e:
                print(f"Espeak Voice output failed: {e}")

if __name__ == "__main__":
    voice = ChibiVoice()
    voice.speak("Hello! I am CHIBI, your high-quality autonomous desktop companion.")
