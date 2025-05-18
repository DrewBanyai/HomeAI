#########
__author__ = "Drew Banyai <DrewBanyai@gmail.com>"
__version__ = "v0.02"
#########

#  If we've passed in an argument, use the first argument to set the current working directory
import sys
import os
if (len(sys.argv) > 1):
    os.chdir(sys.argv[1])

#  Import Helper functionality
from Helper import *

#  Import Speech Detector
from SpeechDetector import SpeechDetector
from TextToSpeech import TextToSpeech
from Commands import ExecuteCommand
from AlarmManager import AlarmManager

#  The primary HomeAI class
class HomeAI:
    def __init__(self):
        self.TextToSpeech = None
        self.SpeechDetector = None
        self.Listening = False
        self.Exit = False
        self.SpeechQueue = []
        self.AlarmManager = AlarmManager(self.AddSpeechString)
        self.Initialize()


    def Respond(self, query):
        #  Confirm that the query string begins with the name of the AI. If not, return out
        queryCheck = StringBeginsWithAIName(query)
        if (queryCheck[0] == False):
            print("Invalid Query Detected (does not begin with AI name): " + query + "\n")
            return
        
        #  Determine the command after the AI name in the full voice text, then pass it to our command execution function.
        queryString = queryCheck[1]
        if (ExecuteCommand(queryString, self.AddSpeechString, self.Shutdown, self.SetAlarm) == False):
            print("Unknown Query Detected: " + queryString)


    def AddSpeechString(self, string):
        self.SpeechQueue.append(string)

    def Shutdown(self):
        print("Shutting down program...")
        self.Exit = True

    def SetAlarm(self, alarmSetting, alarmTime):
        self.AlarmManager.SetAlarm(alarmSetting, alarmTime)


    def Initialize(self):
        print("Initializing:")

        print("Loading Text to Speech generation system...")
        self.TextToSpeech = TextToSpeech()

        print("Loading speech recognition system...")
        self.SpeechDetector = SpeechDetector()

        print("Initialization Complete: Home AI is ready to begin listening...")

        #print("Greeting user...")
        #self.TextToSpeech.Speak(GeneralGreeting())

        self.MainLoop()


    def MainLoop(self):
        while self.Exit == False:
            if (len(self.SpeechQueue) > 0):
                self.Listening = False
                print("Stopping listening service while producing speech...")
                self.SpeechDetector.StopListening(True)
                while (len(self.SpeechQueue) > 0):
                    text = self.SpeechQueue.pop(0)
                    self.TextToSpeech.Speak(text)
            
            if (self.Listening == False):
                self.Listening = True
                if self.SpeechDetector.BeginListening(self.Respond) == False:
                    print("Failed to begin listening. Please ensure you have a working microphone installed on this device.")
                    self.Exit = True
                else:
                    print("Beginning to listen using speech recognition system...\n")
        self.SpeechDetector.StopListening(True)

#  Instantiate the AI
homeAI = HomeAI()