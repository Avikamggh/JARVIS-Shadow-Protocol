"""
JARVIS Voice Module — TTS output + Speech Recognition input
"""
import subprocess
import threading
import re
import os

# Try importing speech recognition
try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


class JarvisVoice:
    """Handle JARVIS voice output (TTS) and input (STT)."""

    def __init__(self, enabled=True, voice_name="Daniel", rate=195):
        self.enabled = enabled
        self.voice_name = voice_name
        self.rate = rate
        self._current_process = None
        self.listening = False
        
        # Speech recognition setup
        if SR_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 1.0
        else:
            self.recognizer = None

    # ── TEXT TO SPEECH ────────────────────────────────────────────────────

    def speak(self, text, async_mode=True):
        if not self.enabled: return
        clean = self._clean_for_speech(text)
        if not clean.strip(): return
        self.stop()
        if async_mode:
            t = threading.Thread(target=self._say, args=(clean,), daemon=True)
            t.start()
        else:
            self._say(clean)

    def _say(self, text):
        try:
            self._current_process = subprocess.Popen(
                ["say", "-v", self.voice_name, "-r", str(self.rate), text],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._current_process.wait()
        except: pass
        finally: self._current_process = None

    def stop(self):
        if self._current_process:
            try: self._current_process.terminate()
            except: pass
            self._current_process = None

    def _clean_for_speech(self, text):
        text = re.sub(r'```[\s\S]*?```', 'code block omitted', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'#{1,6}\s+', '', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 500: text = text[:500] + ". And more."
        return text.strip()

    # ── SPEECH TO TEXT ────────────────────────────────────────────────────

    def can_listen(self):
        """Check if speech recognition is available."""
        return SR_AVAILABLE and self.recognizer is not None

    def listen(self, timeout=5, phrase_timeout=10):
        """Listen for speech and return recognized text."""
        if not self.can_listen():
            return None, "Speech recognition not available. Install: pip install SpeechRecognition PyAudio"

        self.listening = True
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise briefly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for speech
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_timeout)

            # Recognize using Google Speech API (free)
            try:
                text = self.recognizer.recognize_google(audio)
                return text, None
            except sr.UnknownValueError:
                return None, "Couldn't understand. Please speak clearly."
            except sr.RequestError as e:
                return None, f"Speech service error: {e}"

        except sr.WaitTimeoutError:
            return None, "No speech detected. Timed out."
        except OSError as e:
            if "No Default Input Device" in str(e) or "PortAudio" in str(e):
                return None, "No microphone found. Check your audio input settings."
            return None, f"Microphone error: {e}"
        except Exception as e:
            return None, f"Voice input error: {e}"
        finally:
            self.listening = False

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    def set_voice(self, name):
        self.voice_name = name
