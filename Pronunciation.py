def GetTimeNaturalEnglish(currentTime):
    h = str(currentTime.hour - 12) if (currentTime.hour > 12) else str(currentTime.hour)
    m = "" if (currentTime.minute == 0) else (("O " + str(currentTime.minute)) if (currentTime.minute < 10) else str(currentTime.minute))
    ap = "P M" if (currentTime.hour > 12) else "A M"
    return h + " " + m + " " + ap

PRONUNCIATION_KRAKEN_DOT_COM = "Crackin dot com"

PRONUNCIATION_CRYPTO_NAMES = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "LTC": "Litecoin",
    "NANO": "Nano",
    "XBTUSD": "Bitcoin",
    "ETHUSD": "Ethereum",
    "NANOUSD": "Nano"
}

def GetCryptoName(name):
    if (name in PRONUNCIATION_CRYPTO_NAMES):
        return PRONUNCIATION_CRYPTO_NAMES[name]
    return name