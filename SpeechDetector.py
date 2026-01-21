import threading
import json
import os

#  Import Offline Speech Recognizer (through Vosk)
import speech_recognition as sr

#  Import Vosk module
from vosk import SetLogLevel, Model, KaldiRecognizer

from Helper import IsJSON, log_debug_message


class SpeechDetector:
    def __init__(self):
        self.Recognizer = None
        self.Microphone = None
        self.QueryCallback = None
        self.Exit = False
        self.ListeningPaused = False
        self.StopListening = None
        
        # Load the model once during initialization
        log_debug_message("SpeechDetector", "Loading Vosk model...")
        model_path = os.path.join(os.getcwd(), "model")
        if not os.path.exists(model_path):
            log_debug_message("SpeechDetector", f"ERROR: model directory not found at {model_path}")
            self.model = None
        else:
            SetLogLevel(-1)
            self.model = Model(model_path)
            log_debug_message("SpeechDetector", "Vosk model loaded successfully.")
            
        self.Initialize()

    def Initialize(self):
        self.Recognizer = sr.Recognizer()
        self.Recognizer.pause_threshold = 1
        self.Recognizer.energy_threshold = 250
        self.Recognizer.dynamic_energy_threshold = False
        self.Microphone = sr.Microphone(0)
        
    def BeginListening(self, queryCallback):
        self.QueryCallback = queryCallback
        if not self.model:
            log_debug_message("SpeechDetector", "ERROR: Cannot listen because the speech model failed to load.")
            return False

        try:
            # If we were already listening, stop first
            if self.StopListening:
                try:
                    self.StopListening(wait_for_stop=False)
                except:
                    pass
            
            with self.Microphone as source:
                self.Recognizer.adjust_for_ambient_noise(source)
            self.StopListening = self.Recognizer.listen_in_background(self.Microphone, self.ProcessAudioInThread, 5)
            return True
        except Exception as e:
            log_debug_message("SpeechDetector", f"ERROR: Failed to begin listening: {e}")
            return False

    def Shutdown(self):
        """Stops the background listener thread."""
        log_debug_message("SpeechDetector", "Shutdown requested for SpeechDetector...")
        self.Exit = True
        if self.StopListening:
            log_debug_message("SpeechDetector", "Stopping background listener...")
            # Set wait_for_stop to False to avoid hanging if the thread is stuck
            self.StopListening(wait_for_stop=False)
            self.StopListening = None
            log_debug_message("SpeechDetector", "Background listener stopped.")

    def ProcessAudioInThread(self, recognizer, audio):
        if self.Exit:
            return

        log_debug_message("SpeechDetector", "Detected voice audio. Attempting to process audio into text...")
        
        # Using daemon=True so the application can exit even if processing is mid-flight
        processThread = threading.Thread(
            target=self.ProcessAudio, 
            args=(recognizer, audio), 
            name="AudioProcessingThread",
            daemon=True
        )
        processThread.start()

    def ProcessAudio(self, recognizer, audio):
        if (self.ListeningPaused == True or self.Exit == True):
            return

        if (self.QueryCallback == None):
            log_debug_message("SpeechDetector", "ERROR: Received audio to process, but there is no query callback.")
            return
        
        if (audio == None):
            log_debug_message("SpeechDetector", "ERROR: Received audio to process, but the audio data is empty.")
            return
        
        try:
            # Create recognizer with the pre-loaded model
            vosk_recognizer = KaldiRecognizer(self.model, audio.sample_rate)

            # Process audio data
            raw_audio_data = audio.get_raw_data(convert_rate=audio.sample_rate, convert_width=2)
            vosk_recognizer.AcceptWaveform(raw_audio_data)
            
            # Get result
            result_json = vosk_recognizer.Result()
            resultDict = json.loads(result_json)
            query = resultDict.get("text", "").lower()

            if (self.QueryCallback != None and len(query) > 0 and not self.Exit):
                self.QueryCallback(query)
        except Exception as e:
            log_debug_message("SpeechDetector", f"ERROR: Failed to process user voice query: {e}")
