import threading
from Helper import IsJSON
import json
import os

#  Import Offline Speech Recognizer (through Vosk)
try:
    import speech_recognition as sr
except:
    os.system('pip install speechRecognition')
    import speech_recognition as sr

#  Import Vosk module
try:
    from vosk import Model
except:
    os.system('pip install vosk')
    from vosk import Model


class SpeechDetector:
    def __init__(self):
        self.Recognizer = None
        self.Microphone = None
        self.QueryCallback = None
        self.Initialize()

    def Initialize(self):
        self.Recognizer = sr.Recognizer()
        self.Recognizer.vosk_model = Model("model")
        self.Recognizer.pause_threshold = 1
        self.Recognizer.energy_threshold = 300
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
        print("Detected voice audio. Attempting to process audio into text...")
        
        processThread = threading.Thread(target=self.ProcessAudio, args=(recognizer, audio))
        processThread.start()

    def ProcessAudio(self, recognizer, audio):
        if (self.QueryCallback == None):
            print("ERROR: Received audio to process, but there is no query callback to call with the data if we recognized it.")
            return
        
        if (audio == None):
            print("ERROR: Received audio to process, but the audio received is empty data.")
            return
        
        try:
            query = recognizer.recognize_vosk(audio, language="en-in").lower()
            if (IsJSON(query)):
                resultDict = json.loads(query)
                query = resultDict["text"]
            print("USER QUERY: \"" + query + "\"")
            if (self.QueryCallback != None and len(query) > 0):
                self.QueryCallback(query)
                self.Microphone = sr.Microphone(0)
        except Exception as e:
            print("ERROR: Failed to process user voice query. Returning to Listening mode")
            print(e)