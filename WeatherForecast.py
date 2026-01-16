from _env import WEATHER_API_SEVEN_DAY_CALL, WEATHER_API_SINGLE_DAY_CALL, WEATHER_CODES
import requests
import json
from datetime import datetime
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

def GetSevenDayForecast():
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

def GetSingleDayForecast():
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

def PrintSevenDayForecast():
    try:
        weather_code_map = WEATHER_CODES
        weather = GetSevenDayForecast()
        
        print("\nDaily Weather Forecast:")
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
            print("\n")
        else:
            log_debug_message("WeatherForecast", "  Daily weather data not available.")

    except requests.exceptions.RequestException as e:
        log_debug_message("WeatherForecast", f"An error occurred: {e}")

def PrintSingleDayForecast():
    try:
        weather_code_map = WEATHER_CODES
        weather = GetSingleDayForecast()
        
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
            print("\n")
        else:
            log_debug_message("WeatherForecast", "  Daily weather data not available.")

    except requests.exceptions.RequestException as e:
        log_debug_message("WeatherForecast", f"An error occurred: {e}")

def SevenDayForecastString():
    try:
        weather_code_map = WEATHER_CODES
        weather = GetSevenDayForecast()
        
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

def SevenDayForecastJSON():
    try:
        weather = GetSevenDayForecast()
        
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

def SingleDayForecastString():
    try:
        weather_code_map = WEATHER_CODES
        weather = GetSingleDayForecast()
        
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

if __name__ == "__main__":
    PrintSevenDayForecast()
    seven_day_forecast = SevenDayForecastString()
    log_debug_message("WeatherForecast", seven_day_forecast)
    PrintSingleDayForecast()
    single_day_forecast = SingleDayForecastString()
    log_debug_message("WeatherForecast", single_day_forecast)