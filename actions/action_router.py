# actions/action_router.py
import webbrowser
import datetime
import requests

def handle_intent(intent, raw_text=None):
    """
    Handles app or command-based intents.
    """
    if "weather" in intent:
        return get_weather()

    elif "youtube" in intent or "music" in intent:
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube 🎵"

    elif "whatsapp" in intent:
        webbrowser.open("https://web.whatsapp.com/")
        return "Opening WhatsApp 💬"

    elif "time" in intent:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {now}."

    else:
        return "Sorry, I can't perform that action yet."

def get_weather(city="Bangalore"):
    """
    Fetches weather using OpenWeatherMap API (replace with your API key).
    """
    API_KEY = "YOUR_OPENWEATHER_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("main"):
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            return f"The weather in {city} is {desc} with a temperature of {temp}°C."
        else:
            return "Couldn't fetch weather details right now."
    except:
        return "Error fetching weather details."
