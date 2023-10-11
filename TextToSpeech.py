import os

#  Import Offline Text to Speech through pyttsx3
try:
    import pyttsx3
except:
    os.system('pip install pyttsx3')
    import pyttsx3


class TextToSpeech:
    def __init__(self):
        self.VoiceEngine = None
        self.VoiceList = None
        self.Initialize()

    def Initialize(self):
        self.VoiceEngine = pyttsx3.init()
        self.VoiceList = self.VoiceEngine.getProperty("voices")
        self.VoiceEngine.setProperty("voice", self.VoiceList[0].id)
        self.VoiceEngine.setProperty("rate", 150)        

    def Speak(self, string):
        if (self.VoiceEngine == None):
            print("ERROR: Attempted to speak, but my voice engine is not properly loaded. Cancelling speech.")
            return
        
        self.VoiceEngine.say(string)
        self.VoiceEngine.runAndWait()