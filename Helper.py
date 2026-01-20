#  Import standard modules
import datetime
import json
import smtplib
import time
from email.message import EmailMessage
import requests
from playsound3 import *

from _env import AI_NAMES
from Pronunciation import *

from _env import NEWS_API_KEY, GMAIL_EMAIL, GMAIL_APP_PASSWORD, COIN_API_KEY, CRYPTO_ASSET_PAIRS

LOG_FILE_PATH = "debug_log.txt"

def log_debug_message(source: str, message: str):
    """Writes a timestamped debug message with a source identifier to a log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] [{source}]: {message}"
    with open(LOG_FILE_PATH, "a") as f:
        f.write(formatted_message + "\n")

def clear_debug_log():
    """Clears the debug log file by opening it in write mode and closing it."""
    with open(LOG_FILE_PATH, "w") as f:
        pass


def GetDateTime():
    return datetime.datetime.now()


def TellMeTheTime(speechCallback):
    try:
        currentTime = GetDateTime()
        timeStatement = "The time is " + GetTimeNaturalEnglish(currentTime)
        speechCallback(timeStatement)
    except Exception as e:
        log_debug_message("Helper", str(e))


def GeneralTimeOfDay():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Morning"
    elif hour >= 12 and hour < 18:
        return "Afternoon"
    else:
        return "Evening"

def ConvertHourTo24Hour(hour, ap):
    return hour - (12 if (hour == 12) else 0) + (0 if (ap == "am") else 12)


def ChangeTime(dt, hour, minute, second, microsecond):
    log_debug_message("Helper", "ChangeTime: test")


def IsAINameDefined():
    try:
        AI_NAMES[0]
    except:
        log_debug_message("Helper", "No AI_NAMES entries provided. Please provide this in _env.py ...")
        return False
    return True


def GeneralGreeting():
    generalGreeting = ""
    generalGreeting += "Good " + GeneralTimeOfDay() + ". "
    #generalGreeting += ("You may call me " + AI_NAMES[0] + ". ") if IsAINameDefined() else ("")
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
        log_debug_message("Helper", "No NEWS_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://newsapi.org/\n")
        return False
    if NEWS_API_KEY == None:
        log_debug_message("Helper", "No NEWS_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://newsapi.org/\n")
        return False
    return True

def IsCoinApiKeyDefined():
    try:
        COIN_API_KEY
    except NameError:
        log_debug_message("Helper", "No COIN_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://www.coinapi.io/\n")
        return False
    if COIN_API_KEY == None:
        log_debug_message("Helper", "No COIN_API_KEY provided. Please provide this in the User Defined Data section above. You can acquire a key for free at https://www.coinapi.io/\n")
        return False
    return True

def AreCryptoPairsDefined():
    try:
        CRYPTO_ASSET_PAIRS
        CRYPTO_ASSET_PAIRS[0]
    except Exception:
        log_debug_message("Helper", "No CRYPTO_ASSET_PAIRS provided. Please provide this in the User Defined Data section above. Value should be an array of tuples, where each tuple is like so: (\"BTC\", \"USD\", 1) where the third value is the number of decimal places to round the price to\n")
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
        if ('title' in responseJson and responseJson['title'] == 'Forbidden'):
            raise Exception("403 Forbidden error when requesting crypto prices. Please check your Coin API Key and Account")
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
        log_debug_message("Helper", str(priceDataJson))
        speechCallback("Crypto price data acquired from " + PRONUNCIATION_KRAKEN_DOT_COM)
    except Exception as e:
        log_debug_message("Helper", "GET CRYPTO PRICES ERROR")
        log_debug_message("Helper", str(e))


def IsGmailLoginDefined():
    try:
        GMAIL_EMAIL
        GMAIL_APP_PASSWORD
    except Exception as e:
        log_debug_message("Helper", "No GMAIL_LOGIN or GMAIL_APP_PASSWORD data provided. Please provide this in the User Defined Data section above. You can acquire an account for free at https://mail.google.com/\n")
        return False
    if ((GMAIL_EMAIL == None) or (GMAIL_APP_PASSWORD == None)):
        log_debug_message("Helper", "No GMAIL_LOGIN or GMAIL_APP_PASSWORD data provided. Please provide this in the User Defined Data section above. You can acquire an account for free at https://mail.google.com/\n")
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
        log_debug_message("Helper", "EMAIL SEND EXCEPTION")
        log_debug_message("Helper", str(e))

def Sleep(seconds):
    time.sleep(seconds)