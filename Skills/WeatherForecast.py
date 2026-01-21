import requests
import json
from datetime import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _env import WEATHER_API_SEVEN_DAY_CALL, WEATHER_API_SINGLE_DAY_CALL, WEATHER_CODES
from Helper import log_debug_message

class WeatherData:
    def __init__(self, api_data):
        self.latitude = api_data.get('latitude')
        self.longitude = api_data.get('longitude')
        self.generationtime_ms = api_data.get('generationtime_ms')
        self.utc_offset_seconds = api_data.get('utc_offset_seconds')
        self.timezone = api_data.get('timezone')
        self.timezone_abbreviation = api_data.get('timezone_abbreviation')
        self.elevation = api_data.get('elevation')
        self.daily_units = api_data.get('daily_units', {})
        
        daily_data = api_data.get('daily', {})
        self.time = daily_data.get('time')
        self.weather_code = daily_data.get('weather_code')
        self.temperature_2m_max = [round(temp) for temp in daily_data.get('temperature_2m_max')] if daily_data.get('temperature_2m_max') else None
        self.temperature_2m_min = [round(temp) for temp in daily_data.get('temperature_2m_min')] if daily_data.get('temperature_2m_min') else None

class Skill_WeatherForecast:
    def __init__(self):
        self.commandPossibilities = {
            # ACTUAL COMMAND NAMES
            "seven day forecast" : "SEVEN DAY FORECAST",
            "single day forecast" : "SINGLE DAY FORECAST",

            #  Alternates: SEVEN DAY FORECAST
            "weather forecast": "SEVEN DAY FORECAST",
            "what's the weather forecast": "SEVEN DAY FORECAST",
            "how's the weather for the next seven days": "SEVEN DAY FORECAST",
            "give me the weather report": "SEVEN DAY FORECAST",
            "what's the seven day forecast": "SEVEN DAY FORECAST",

            #  Alternates: SINGLE DAY FORECAST
            "single day forecasts": "SINGLE DAY FORECAST",
            "weather forecast today": "SINGLE DAY FORECAST",
            "weather forecasts today": "SINGLE DAY FORECAST",
            "what's the weather": "SINGLE DAY FORECAST",
            "what's the weather today": "SINGLE DAY FORECAST",
            "what's today's weather": "SINGLE DAY FORECAST",
            "how's the weather today": "SINGLE DAY FORECAST",
            "give me the weather report for today": "SINGLE DAY FORECAST",
            "what's the weather": "SINGLE DAY FORECAST",
        }
        self.commandActionMap = {
            "SEVEN DAY FORECAST": self.SevenDayForecastString,
            "SINGLE DAY FORECAST": self.SingleDayForecastString,
        }
        self.PartialCommands = {}


    def GetSevenDayForecast(self):
        api_call = WEATHER_API_SEVEN_DAY_CALL
        log_debug_message("WeatherForecast", "Fetching the seven day forecast from [api.open-meteo.com]")

        try:
            response = requests.get(api_call)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            log_debug_message("WeatherForecast", f"Report: {data}")
            weather = WeatherData(data)
            return weather

        except requests.exceptions.RequestException as e:
            log_debug_message("WeatherForecast", f"An error occurred: {e}")


    def GetSingleDayForecast(self):
        api_call = WEATHER_API_SINGLE_DAY_CALL
        log_debug_message("WeatherForecast", "Fetching the daily forecast for today from [api.open-meteo.com]")

        try:
            response = requests.get(api_call)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            log_debug_message("WeatherForecast", f"Report: {data}")
            weather = WeatherData(data)
            return weather

        except requests.exceptions.RequestException as e:
            log_debug_message("WeatherForecast", f"An error occurred: {e}")


    def PrintSevenDayForecast(self):
        try:
            weather_code_map = WEATHER_CODES
            weather = self.GetSevenDayForecast()
            
            log_debug_message("WeatherForecast", "\nDaily Weather Forecast:")
            if weather.time and weather.temperature_2m_max and weather.temperature_2m_min and weather.weather_code:
                log_debug_message("WeatherForecast", f"{'Day':<12} {'Temp (Max)':<15} {'Temp (Min)':<15} {'Weather':<25}")
                log_debug_message("WeatherForecast", "-" * 79)
                for i in range(len(weather.time)):
                    date_obj = datetime.fromisoformat(weather.time[i])
                    day_of_week = date_obj.strftime('%A')
                    code_description = weather_code_map.get(weather.weather_code[i], f"Unknown ({weather.weather_code[i]})")
                    log_debug_message("WeatherForecast", 
                        f"{day_of_week:<12} "
                        f"{weather.temperature_2m_max[i]:<15} "
                        f"{weather.temperature_2m_min[i]:<15} "
                        f"{code_description:<25}"
                    )
                log_debug_message("WeatherForecast", "\n")
            else:
                log_debug_message("WeatherForecast", "  Daily weather data not available.")

        except requests.exceptions.RequestException as e:
            log_debug_message("WeatherForecast", f"An error occurred: {e}")


    def PrintSingleDayForecast(self):
        try:
            weather_code_map = WEATHER_CODES
            weather = self.GetSingleDayForecast()
            
            log_debug_message("WeatherForecast", "\nDaily Weather Forecast:")
            if weather.time and weather.temperature_2m_max and weather.temperature_2m_min and weather.weather_code:
                log_debug_message("WeatherForecast", f"{'Day':<12} {'Temp (Max)':<15} {'Temp (Min)':<15} {'Weather':<25}")
                log_debug_message("WeatherForecast", "-" * 79)
                for i in range(len(weather.time)):
                    date_obj = datetime.fromisoformat(weather.time[i])
                    day_of_week = date_obj.strftime('%A')
                    code_description = weather_code_map.get(weather.weather_code[i], f"Unknown ({weather.weather_code[i]})")
                    log_debug_message("WeatherForecast", 
                        f"{day_of_week:<12} "
                        f"{weather.temperature_2m_max[i]:<15} "
                        f"{weather.temperature_2m_min[i]:<15} "
                        f"{code_description:<25}"
                    )
                log_debug_message("WeatherForecast", "\n")
            else:
                log_debug_message("WeatherForecast", "  Daily weather data not available.")

        except requests.exceptions.RequestException as e:
            log_debug_message("WeatherForecast", f"An error occurred: {e}")


    def SevenDayForecastJSON(self, weather):
        try:
            if weather.time and weather.temperature_2m_max and weather.temperature_2m_min and weather.weather_code:
                weather_data = []
                for i in range(len(weather.time)):
                    date_obj = datetime.fromisoformat(weather.time[i])
                    day_name = date_obj.strftime('%A')
                    weather_data.append({
                        "code": weather.weather_code[i],
                        "high": weather.temperature_2m_max[i],
                        "low": weather.temperature_2m_min[i],
                        "day": day_name
                    })
                return json.dumps(weather_data)
            else:
                return None

        except Exception as e:
            log_debug_message("WeatherForecast", f"An error occurred in SevenDayForecastJSON: {e}")
            return None


    def SevenDayForecastString(self, callbacks):
        try:
            weather_code_map = WEATHER_CODES
            weather = self.GetSevenDayForecast()

            cb = callbacks.get("SevenDayForecast")
            if weather and cb:
                weather_json = self.SevenDayForecastJSON(weather)
                if weather_json:
                    cb(weather_json)
            
            forecast_str = "Weather for the next seven days:\n"
            if weather.time and weather.temperature_2m_max and weather.temperature_2m_min and weather.weather_code:
                for i in range(len(weather.time)):
                    date_obj = datetime.fromisoformat(weather.time[i])
                    day_of_week = date_obj.strftime('%A')
                    code_description = weather_code_map.get(weather.weather_code[i], f"Unknown ({weather.weather_code[i]})")
                    forecast_str += (f"{day_of_week}, {code_description} with a high of {weather.temperature_2m_max[i]} and low of {weather.temperature_2m_min[i]}.\n")
                return forecast_str
            else:
                return "Sorry, the seven day forecast was not available. Please try again later."

        except requests.exceptions.RequestException as e:
            log_debug_message("WeatherForecast", f"An error occurred: {e}")
            return "Sorry, an error occurred. Please try again later."


    def SingleDayForecastString(self, callbacks):
        try:
            weather_code_map = WEATHER_CODES
            weather = self.GetSingleDayForecast()
            
            forecast_str = "The weather today:\n"
            if weather.time and weather.temperature_2m_max and weather.temperature_2m_min and weather.weather_code:
                for i in range(len(weather.time)):
                    date_obj = datetime.fromisoformat(weather.time[i])
                    day_of_week = date_obj.strftime('%A')
                    code_description = weather_code_map.get(weather.weather_code[i], f"Unknown ({weather.weather_code[i]})")
                    forecast_str += (f"{day_of_week}, {code_description} with a high of {weather.temperature_2m_max[i]} and low of {weather.temperature_2m_min[i]}.\n")
                return forecast_str
            else:
                return "Sorry, the daily forecast was not available. Please try again later."

        except requests.exceptions.RequestException as e:
            log_debug_message("WeatherForecast", f"An error occurred: {e}")
            return "Sorry, an error occurred. Please try again later."