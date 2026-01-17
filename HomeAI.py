#########
__author__ = "Drew Banyai <DrewBanyai@gmail.com>"
__version__ = "v0.03"
#########

# Environment variables
from _env import GREET_USER_ON_STARTUP

#  If we've passed in an argument, use the first argument to set the current working directory
import sys
import os
if (len(sys.argv) > 1):
    os.chdir(sys.argv[1])

#  Import Helper functionality
from Helper import *

# Clear the debug log at the very start of the program
clear_debug_log()

#  Import Speech Detector
from SpeechDetector import SpeechDetector
from TextToSpeech import TextToSpeech
from Commands import ExecuteCommand
from AlarmManager import AlarmManager
from TerminalUI import TerminalUI
from CommandAlternates import AINameAlternates



def StringBeginsWithAIName(string):
    if IsAINameDefined() == False:
        return (False, "")
    
    firstSpace = string.find(" ")
    if (firstSpace == -1):
        return (False, "")
    
    for alt in AINameAlternates:
        nameLength = len(alt + " ")
    
        # Search for the first instance of the name. It is possible that other words could be picked up prior and we should ignore anything before the wake word.
        nameIndex = string.find(alt)
        if (nameIndex == -1):
            continue
    
        if (string[nameIndex:nameIndex+nameLength].lower() == (alt + " ").lower()):
            return (True, string[nameIndex+nameLength:len(string)])
    
    return (False, "")


#  The primary HomeAI class
class HomeAI:
    def __init__(self):
        self.TextToSpeech = None
        self.SpeechDetector = None
        self.Exit = False
        self.SpeechQueue = []
        self.AlarmManager = None
        self.ui = None


    def Respond(self, query):
        if self.ui:
            self.ui.call_from_thread(self.ui.update_status, "Thinking...")
        #  Confirm that the query string begins with the name of the AI. If not, return out
        queryCheck = StringBeginsWithAIName(query)
        if (queryCheck[0] == False):
            log_debug_message("HomeAI", f"Invalid Query Detected (does not begin with AI name): {query}\n")
            if self.ui:
                self.ui.call_from_thread(self.ui.update_status, "Listening...")
            return
        
        #  Determine the command after the AI name in the full voice text, then pass it to our command execution function.
        queryString = queryCheck[1]
        if (ExecuteCommand(queryString, self.AddSpeechString, self.Shutdown, self.SetAlarm, self.WeatherUpdateCallback) == False):
            log_debug_message("HomeAI", f"Unknown Query Detected: {queryString}")
            return
        
        # Add the full query to the command history in the UI
        if self.ui:
            self.ui.call_from_thread(self.ui.add_line_to_history, "COMMAND: ", queryString)

        # If we have nothing to speak, return to listening status in the UI
        if (len(self.SpeechQueue) == 0):
            if self.ui:
                self.ui.call_from_thread(self.ui.update_status, "Listening...")
            log_debug_message("HomeAI", "Thinking complete. Listening...")


    def AddSpeechString(self, string):
        self.SpeechQueue.append(string)

    def WeatherUpdateCallback(self, weather_data_json):
        if self.ui:
            self.ui.call_from_thread(self.ui.update_weather_report, weather_data_json)

    def Shutdown(self):
        log_debug_message("HomeAI", "Shutting down program...")
        self.Exit = True

    def SetAlarm(self, alarmSetting, alarmTime):
        self.AlarmManager.SetAlarm(alarmSetting, alarmTime)


    def Initialize(self):
        if self.ui:
            self.ui.call_from_thread(self.ui.update_status, "Initializing HomeAI...")
        log_debug_message("Initialize", "Initializing HomeAI...")

        if self.ui:
            self.ui.call_from_thread(self.ui.update_status, "Loading Alarm Manager system...")
        log_debug_message("Initialize", "Loading Alarm Manager system...")
        self.AlarmManager = AlarmManager(self.AddSpeechString)

        if self.ui:
            self.ui.call_from_thread(self.ui.update_status, "Loading Text to Speech generation system...")
        log_debug_message("Initialize", "Loading Text to Speech generation system...")
        self.TextToSpeech = TextToSpeech()

        if self.ui:
            self.ui.call_from_thread(self.ui.update_status, "Loading speech recognition system...")
        log_debug_message("Initialize", "Loading speech recognition system...")
        self.SpeechDetector = SpeechDetector()
        self.SpeechDetector.BeginListening(self.Respond)

        if self.ui:
            self.ui.call_from_thread(self.ui.update_status, "Initialization Complete. Listening... ")
        log_debug_message("Initialize", "Initialization Complete. Listening... ")

        if GREET_USER_ON_STARTUP == True:
            self.TextToSpeech.Speak(GeneralGreeting())


    def run(self):
        """Initializes and runs the main application loop."""
        self.Initialize()
        self.MainLoop()


    def MainLoop(self):
        while self.Exit == False:
            if (len(self.SpeechQueue) > 0):
                log_debug_message("MainLoop", f"Detected {len(self.SpeechQueue)} items in speech queue.")
                if self.ui:
                    self.ui.call_from_thread(self.ui.update_status, "Speaking...")
                log_debug_message("MainLoop", "Speaking...")

                #self.SpeechDetector.StopListening(True)
                self.SpeechDetector.ListeningPaused = True

                while (len(self.SpeechQueue) > 0):
                    text = self.SpeechQueue.pop(0)

                    # Add the response to the conversation history in the UI
                    if self.ui:
                        self.ui.call_from_thread(self.ui.add_line_to_history, "RESPONSE: ", text)
                    log_debug_message("MainLoop", f"RESPONSE: {text}")

                    self.TextToSpeech.Speak(text)
                log_debug_message("MainLoop", "Cleared the speech queue. Returning to listening mode...")
            
            if (self.SpeechDetector.ListeningPaused == True):
                #if self.SpeechDetector.BeginListening(self.Respond) == False:
                #    log_debug_message("MainLoop", "Failed to begin listening. Please ensure you have a working microphone installed on this device.")
                #    self.Exit = True
                #else:
                self.SpeechDetector.ListeningPaused = False
                if self.ui:
                    self.ui.call_from_thread(self.ui.update_status, "Listening...")
                log_debug_message("MainLoop", "Listening...")

        self.AlarmManager.Exit = True
        self.SpeechDetector.StopListening(True)

if __name__ == "__main__":
    # Instantiate the AI
    homeAI = HomeAI()
    
    # Instantiate the UI, passing the AI instance to it
    ui = TerminalUI(home_ai_instance=homeAI)

    # Run the UI (this will also start the AI's initialization and main loop on_mount)
    ui.run()