#  NEWS_API_KEY should be a string of your NewsApi.org API key. You can acquire a key for free at https://newsapi.org/
NEWS_API_KEY = None

#  COIN_API_KEY should be a string of your CoinAPI.io API key. You can acquire a key for free at https://www.coinapi.io/
COIN_API_KEY = None
CRYPTO_ASSET_PAIRS = [
    ( "BTC", "USD", 1 ),
    #( "ETH", "USD", 1 ),
    #( "LTC", "USD", 2 ),
    #( "NANO", "USD", 3 ),
]

#  GMAIL LOGIN should be a two-item tuple where the first is the string of your gmail account email and the second is your email account password
GMAIL_EMAIL = None
GMAIL_APP_PASSWORD = None

#  AI_NAME should be a string representing a word which you use to refer to the AI. By default, this is "Frank"
AI_NAME = "Frank"

WEATHER_API_CALL="https://api.open-meteo.com/v1/forecast?latitude=42.0695&longitude=-76.1547&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=America%2FNew_York&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    56: "Slight Freezing Drizzle",
    57: "HeavyFreezing Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Slight Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Slight Snow Showers",
    86: "Heavy Snow Showers",
    95: "Slight to Moderate Thunderstorm",
    96: "Slight Thunderstorm and Hail",
    99: "Heavy Thunderstorm and Hail",
}