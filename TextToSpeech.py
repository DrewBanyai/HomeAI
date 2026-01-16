#  Import Offline Text to Speech through pyttsx3
import pyttsx3
from Helper import log_debug_message


class TextToSpeech:
    def Speak(self, string):
        """
        Initializes a new voice engine, speaks the given string, and shuts down.
        This is a robust way to handle pyttsx3's state issues.
        """
        try:
            engine = pyttsx3.init('sapi5')
            voice_list = engine.getProperty("voices")
            engine.setProperty("voice", voice_list[0].id)
            engine.setProperty("rate", 150)
            engine.say(string)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            log_debug_message("TextToSpeech", f"ERROR: An error occurred in the text-to-speech engine: {e}")