from Helper import GetAIName, TellMeTheTime, GetNewsTopHeadlines, SendTestEmail, GetCryptoPrices, IsGmailLoginDefined
from _env import GMAIL_EMAIL
from CommandAlternates import CommandAlternates

def ExecuteCommand(command, speechCallback, shutdownCallback):
    #  If we use an alternate command, switch over to the official command string
    if (command in CommandAlternates):
        print("Switching command: [" + command + "] > [" + CommandAlternates[command] + "]")
        command = CommandAlternates[command]

    if (command == "can you hear me"):
        speechCallback("I can hear you. I listen for any command following my name, " + GetAIName())
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
    
    if (command == "shut down"):
        shutdownCallback()
        return True

    return False