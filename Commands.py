from _env import AI_NAMES
from Helper import TellMeTheTime, GetNewsTopHeadlines, SendTestEmail, GetCryptoPrices, IsGmailLoginDefined, log_debug_message
from _env import GMAIL_EMAIL
from CommandAlternates import CommandAlternates, PartialAlternates
from WeatherForecast import SevenDayForecastString, SingleDayForecastString, SevenDayForecastJSON
from ConvertStringToTime import ConvertStringToTime

class CommandCallback:
    def __init__(self, callbackType, callback):
        log_debug_message("Commands", "Command Callback __init__")

def ExecuteCommand(command, speechCallback, shutdownCallback, alarmCallback, weatherUpdateCallback=None):
    log_debug_message("Commands", "Execute command: [" + command + "]")
    
    #  If we use an alternate command, switch over to the official command string
    if (command in CommandAlternates):
        log_debug_message("Commands", "Switching command: [" + command + "] > [" + CommandAlternates[command] + "]")
        command = CommandAlternates[command]

    #  Check for "partial commands" first, commands which begin with a command trigger term and then include details
    partialCheck = PartialCommandCheck(command, speechCallback, shutdownCallback)
    if (partialCheck and partialCheck[0] == True):
        partialCommand = partialCheck[1]
        partialDetails = partialCheck[2]
        log_debug_message("Commands", "Partial Command detected and parsed! Command [" + partialCommand + "], Details: [" + partialDetails + "]")

        if (partialCommand == "set an alarm for"):
            timeConvert = ConvertStringToTime(partialDetails)
            if (timeConvert.Error != None):
                log_debug_message("Commands", "Time Conversion Error: " + timeConvert.Error)
                return False
            else:
                log_debug_message("Commands", f"Time Convert complete: {timeConvert.DateTime}")
                alarmCallback(timeConvert.TimeSetting, timeConvert.DateTime)
                return True

    if (command == "can you hear me"):
        speechCallback("I can hear you. I listen for any command following my name, " + AI_NAMES[0])
        return True

    if (command == "what time is it"):
        TellMeTheTime(speechCallback)
        return True

    if (command == "give me the headlines"):
        headlineList = GetNewsTopHeadlines(speechCallback)
        for h in headlineList:
            speechCallback(h)
        return True
    
    if (command == "get crypto prices"):
        priceList = GetCryptoPrices(speechCallback)
        for p in priceList:
            speechCallback("The current exchange rate of " + p[0] + " to " + p[1] + " is " + p[2])
        return True
    
    if (command == "send a test email"):
        if IsGmailLoginDefined() == True:
            speechCallback("Sending test email to " + GMAIL_EMAIL)
            SendTestEmail(GMAIL_EMAIL, "Subject Test", "This is a test email.")
        return True
    
    if (command == "seven day forecast"):
        forecast_string = SevenDayForecastString()
        speechCallback(forecast_string)
        if weatherUpdateCallback:
            weather_json = SevenDayForecastJSON()
            if weather_json:
                weatherUpdateCallback(weather_json)
        return True
    
    if (command == "single day forecast"):
        forecast_string = SingleDayForecastString()
        speechCallback(forecast_string)
        return True

    if (command == "shut down"):
        shutdownCallback()
        return True

    return False

def PartialCommandCheck(command, speechCallback, shutdownCallback):
    try:
        details = ""
        for alt in PartialAlternates:
            portion = command[0:len(alt) + 1]
            if (portion == alt + " "):
                details = command[len(alt) + 1:len(command)]
                command = PartialAlternates[alt]
                return (True, command, details)
    except Exception as e:
        log_debug_message("Commands", "PartialCommand exception")
        log_debug_message("Commands", str(e))
    return (False, None, None)