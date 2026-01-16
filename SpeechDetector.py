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
        self.Initialize()

    def Initialize(self):
        self.Recognizer = sr.Recognizer()
        self.Recognizer.pause_threshold = 1
        self.Recognizer.energy_threshold = 250
        self.Recognizer.dynamic_energy_threshold = False
        self.Microphone = sr.Microphone(0)
        
    def BeginListening(self, queryCallback):
        self.QueryCallback = queryCallback
        try:
            with self.Microphone as source:
                self.Recognizer.adjust_for_ambient_noise(source)
            self.StopListening = self.Recognizer.listen_in_background(self.Microphone, self.ProcessAudioInThread, 5)
            return True
        except Exception as e:
            return False

    def ProcessAudioInThread(self, recognizer, audio):
        log_debug_message("SpeechDetector", "Detected voice audio. Attempting to process audio into text...")
        
        processThread = threading.Thread(target=self.ProcessAudio, args=(recognizer, audio))
        processThread.start()

    def ProcessAudio(self, recognizer, audio):
        if (self.QueryCallback == None):
            log_debug_message("SpeechDetector", "ERROR: Received audio to process, but there is no query callback to call with the data if we recognized it.")
            return
        
        if (audio == None):
            log_debug_message("SpeechDetector", "ERROR: Received audio to process, but the audio received is empty data.")
            return
        
        try:
            SetLogLevel(-1)

            # Create vosk model and recognizer
            vosk_model = Model(os.path.join(os.getcwd(), "model"))
            vosk_recognizer = KaldiRecognizer(vosk_model, audio.sample_rate)

            # Process audio data
            # speech_recognition's AudioData needs to be fed to vosk
            raw_audio_data = audio.get_raw_data(convert_rate=audio.sample_rate, convert_width=2)
            vosk_recognizer.AcceptWaveform(raw_audio_data)
            
            # Get result
            result_json = vosk_recognizer.Result()
            resultDict = json.loads(result_json)
            query = resultDict["text"].lower()

            #print("USER QUERY: \"" + query + "\"")
            if (self.QueryCallback != None and len(query) > 0):
                self.QueryCallback(query)
                self.Microphone = sr.Microphone(0)
        except Exception as e:
            log_debug_message("SpeechDetector", "ERROR: Failed to process user voice query. Returning to Listening mode")
            log_debug_message("SpeechDetector", str(e))