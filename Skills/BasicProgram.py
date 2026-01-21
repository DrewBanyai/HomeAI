import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Helper import GetDateTime, log_debug_message
from Pronunciation import GetTimeNaturalEnglish

class Skill_BasicProgram:
    def __init__(self):
        self.commandPossibilities = {
            # ACTUAL COMMAND NAMES
            "shut down" : "SHUT DOWN",
            "tell me the time" : "TELL ME THE TIME",
            "what time is it" : "TELL ME THE TIME"
        }
        self.commandActionMap = {
            "SHUT DOWN": self.Shutdown,
            "TELL ME THE TIME": self.TellMeTheTime
        }
        self.PartialCommands = {}

    def Shutdown(self, callbacks):
        cb = callbacks.get("Shutdown")
        if cb:
            cb()
        return None

    def TellMeTheTime(self, callbacks):
        try:
            currentTime = GetDateTime()
            timeStatement = "The time is " + GetTimeNaturalEnglish(currentTime)
            return timeStatement
        except Exception as e:
            log_debug_message("BasicProgram", "TellMeTheTime exception: " + str(e))
            return None