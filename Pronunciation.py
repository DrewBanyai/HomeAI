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

PRONUNCIATION_WORDS_TO_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "oh": 0,
}

#  Words that, when in a number formed by two words, can be the first word
PRONUNCIATION_WORDS_PART_1_OF_2 = [
    "twenty",
    "thirty",
    "forty",
    "fifty",
    "sixty",
    "seventy",
    "eighty",
    "ninety",
]

#  Words that, when in a number formed by two words, can be the second word
PRONUNCIATION_WORDS_PART_2_OF_2 = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]