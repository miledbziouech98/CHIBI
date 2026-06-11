import os
import subprocess
import shutil
import platform

class YozuVoice:
    def __init__(self, engine="kokoro"):
        self.engine = engine
        self.os_type = platform.system()
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

        # Kokoro specific setup (placeholder for actual kokoro integration)
        self.enabled = self._check_engine()

    def _check_engine(self):
        if self.engine == "kokoro":
            try:
                import kokoro
                return True
            except ImportError:
                return False
        elif self.engine == "piper":
            self.piper_path = os.path.join(self.base_dir, "bin/piper/piper")
            if self.os_type == "Windows":
                 self.piper_path += ".exe"
            self.model_path = os.path.join(self.base_dir, "assets/voice_model.onnx")
            return os.path.exists(self.piper_path) and os.path.exists(self.model_path)
        elif self.engine == "espeak":
            return shutil.which("espeak") is not None
        return False

    def speak(self, text):
        print(f"Yozu says: {text}")
        if not self.enabled:
            print(f"Voice output is disabled ({self.engine} engine or model not found).")
            # Fallback to espeak if available
            if shutil.which("espeak"):
                self.engine = "espeak"
                self.enabled = True
            else:
                return

        if self.engine == "kokoro":
            try:
                from kokoro import KPipeline
                import sounddevice as sd

                # Initialize pipeline if not exists
                if not hasattr(self, 'pipeline'):
                    self.pipeline = KPipeline(lang_code='a') # 'a' for American English

                print(f"Synthesizing with Kokoro: {text}")
                generator = self.pipeline(text, voice='af_sky', speed=1, split_pattern=r'\n+')

                for gs, ps, audio in generator:
                    sd.play(audio, 24000)
                    sd.wait()

            except Exception as e:
                print(f"Kokoro Voice output failed: {e}. Falling back to espeak.")
                self.engine = "espeak"
                self.speak(text)

        elif self.engine == "piper":
            try:
                if self.os_type == "Linux":
                    piper_process = subprocess.Popen(
                        [self.piper_path, "--model", self.model_path, "--output_raw"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL
                    )
                    aplay_process = subprocess.Popen(
                        ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw"],
                        stdin=piper_process.stdout
                    )
                    piper_process.stdin.write(text.encode('utf-8'))
                    piper_process.stdin.close()
                    aplay_process.wait()
                elif self.os_type == "Windows":
                    # On Windows, we can use piper to generate a wav and then play it
                    wav_path = os.path.join(self.base_dir, "temp_voice.wav")
                    subprocess.run(
                        [self.piper_path, "--model", self.model_path, "--output_file", wav_path],
                        input=text.encode('utf-8'),
                        check=True,
                        stderr=subprocess.DEVNULL
                    )
                    # Play using native Windows command or winsound
                    import winsound
                    winsound.PlaySound(wav_path, winsound.SND_FILENAME)
                    os.remove(wav_path)

            except Exception as e:
                print(f"Piper Voice output failed: {e}")

        elif self.engine == "espeak":
            try:
                if self.os_type == "Linux":
                    subprocess.run(["espeak", "-v", "en-us+f3", "-s", "170", "-p", "80", text], check=True)
                elif self.os_type == "Windows":
                     # Windows users often have SAPI5 or can install espeak-ng
                     subprocess.run(["espeak", text], check=True)
            except Exception as e:
                print(f"Espeak Voice output failed: {e}")

if __name__ == "__main__":
    voice = YozuVoice()
    voice.speak("Hello! I am Yozu, your cross-platform autonomous desktop companion.")
