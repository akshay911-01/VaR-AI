# actions/weather_api.py
import requests
import os

OWM_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

def get_weather(city):
    if not OWM_API_KEY:
        return f"[demo] Weather for {city}: 27°C, clear sky (Set OPENWEATHER_API_KEY to get real data)."
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OWM_API_KEY}"
    try:
        r = requests.get(url, timeout=5).json()
        temp = r['main']['temp']
        desc = r['weather'][0]['description']
        return f"Current temperature in {city} is {temp}°C, {desc}."
    except Exception:
        return f"Couldn't fetch weather for {city}."
