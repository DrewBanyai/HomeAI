#  Import standard modules
import datetime
import json
import smtplib
import time
import os
from email.message import EmailMessage
from playsound import *

from CommandAlternates import AINameAlternates
from Pronunciation import *

#  Import requests functionality
try:
    import requests
except:
    os.system('pip install requests')
    import requests

from _env import NEWS_API_KEY, GMAIL_EMAIL, GMAIL_APP_PASSWORD, AI_NAME, COIN_API_KEY, CRYPTO_ASSET_PAIRS


def GetDateTime():
    return datetime.datetime.now()


def TellMeTheTime(speechCallback):
    try:
        currentTime = GetDateTime()
        timeStatement = "The time is " + GetTimeNaturalEnglish(currentTime)
        speechCallback(timeStatement)
    except Exception as e:
        print(e)


def StringBeginsWithAIName(string):
    if IsAINameDefined() == False:
        return False
    
    firstSpace = string.find(" ")
    if (firstSpace == -1):
        return (False, "")
    
    for alt in AINameAlternates:
        nameLength = len(alt + " ")
        if (string[0:nameLength].lower() == (alt + " ").lower()):
            return (True, string[nameLength:len(string)])
    
    if (string[0:nameLength].lower() == (AI_NAME + " ").lower()):
        return (True, string[nameLength:len(string)])
    return (False, "")


def GeneralTimeOfDay():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Morning"
    elif hour >= 12 and hour < 18:
        return "Afternoon"
    else:
        return "Evening"


def IsAINameDefined():
    try:
        AI_NAME
    except NameError:
        print("No AI_NAME provided. Please provide this in the User Defined Data section above.")
        return False
    return True


def GetAIName():
    return AI_NAME if IsAINameDefined() else ""


def GeneralGreeting():
    generalGreeting = ""
    generalGreeting += "Good " + GeneralTimeOfDay() + ". "
    #generalGreeting += ("You may call me " + AI_NAME + ". ") if IsAINameDefined() else ("")
    generalGreeting += "How may I help you?"
    return generalGreeting


def HTTPGet(url, headers=None):
    return requests.get(url, headers=headers)


def JSONLoad(string):
    return json.loads(string)


def IsJSON(string):
  try:
    JSONLoad(string)
  except ValueError as e:
    return False
  return True


def IsNewsApiKeyDefined():
    try:
        NEWS_API_KEY
    except NameError:
        print("No NEWS_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://newsapi.org/\n")
        return False
    if NEWS_API_KEY == None:
        print("No NEWS_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://newsapi.org/\n")
        return False
    return True

def IsCoinApiKeyDefined():
    try:
        COIN_API_KEY
    except NameError:
        print("No COIN_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://www.coinapi.io/\n")
        return False
    if COIN_API_KEY == None:
        print("No COIN_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://www.coinapi.io/\n")
        return False
    return True

def AreCryptoPairsDefined():
    try:
        CRYPTO_ASSET_PAIRS
        CRYPTO_ASSET_PAIRS[0]
    except Exception:
        print("No CRYPTO_ASSET_PAIRS provided. Please provide this in the User Defined Data section above. Value should be an array of tuples, where each tuple is like so: (\"BTC\", \"USD\", 1) where the third value is the number of decimal places to round the price to\n")
        return False
    return True



def GetNewsTopHeadlines(speechCallback):
    if IsNewsApiKeyDefined() == False:
        return []
    
    url = "http://newsapi.org/v2/top-headlines?sources=associated-press&apiKey=" + NEWS_API_KEY
    news = HTTPGet(url).text
    news_dict = JSONLoad(news)
    articles = news_dict["articles"]
    headlineList = []
    headlineList.append("Todays Headlines from The Associated Press")
    for index, headline in enumerate(articles):
        headlineList.append(headline["title"])
        if index == len(articles) - 1:
            break
        headlineList.append("Next headline")
    headlineList.append("These were the top headlines.")
    return headlineList


def GetCryptoPrices(speechCallback):
    if IsCoinApiKeyDefined() == False:
        return []
    if AreCryptoPairsDefined() == False:
        speechCallback("No crypto asset pairs defined.")
        return []
    
    priceList = []
    for c in CRYPTO_ASSET_PAIRS:
        url = "https://rest.coinapi.io/v1/exchangerate/" + c[0] + "/" + c[1]
        headers = {
            "X-CoinAPI-Key": COIN_API_KEY # Replace with your API key
        }
        response = HTTPGet(url, headers)
        responseJson = response.json()
        priceList.append((GetCryptoName(c[0]), GetCryptoName(c[1]), str(round(responseJson["rate"], c[2]))))
    return priceList


def GetCryptoPrices_old(speechCallback):
    assetPairs = [ "xbtusd", "ethusd", "nanousd" ]
    assetPairsStr = ",".join(assetPairs)
    url = "https://api.kraken.com/0/public/AssetPairs?pair=" + assetPairsStr
    try:
        priceData = HTTPGet(url).text
        priceDataJson = JSONLoad(priceData)
        for asset in assetPairs:
            for entry in priceDataJson["result"]:
                if (entry["altname"].lower() == asset):
                    speechCallback("Current Price for asset " + asset + " is ")
        print(priceDataJson)
        speechCallback("Crypto price data acquired from " + PRONUNCIATION_KRAKEN_DOT_COM)
    except Exception as e:
        print("GET CRYPTO PRICES ERROR")
        print(e)


def IsGmailLoginDefined():
    try:
        GMAIL_EMAIL
        GMAIL_APP_PASSWORD
    except Exception as e:
        print("No GMAIL_LOGIN or GMAIL_APP_PASSWORD data provided. Please provide this in the User Defined Data section above. You can acquire an account for free at https://mail.google.com/\n")
        return False
    if ((GMAIL_EMAIL == None) or (GMAIL_APP_PASSWORD == None)):
        print("No GMAIL_LOGIN or GMAIL_APP_PASSWORD data provided. Please provide this in the User Defined Data section above. You can acquire an account for free at https://mail.google.com/\n")
        return False
    return True


def SendTestEmail(sendTo, subject, messageText):
    if IsGmailLoginDefined() == False:
        return
    
    msg = EmailMessage()
    msg.set_content(messageText)
    msg['Subject'] = subject
    msg['From'] = GMAIL_EMAIL
    msg['To'] = sendTo
    
    # Send the message via our own SMTP server.
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("EMAIL SEND EXCEPTION")
        print(e)

def Sleep(seconds):
    time.sleep(seconds)