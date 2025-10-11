# actions/action_router.py
import webbrowser
import datetime
import requests
import os
import subprocess
import platform

def handle_intent(intent, raw_text=None):
    """
    Handles app or command-based intents.
    """
    if intent == "weather":
        return get_weather()

    elif intent == "youtube" or intent == "music":
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube 🎵"

    elif intent == "whatsapp":
        webbrowser.open("https://web.whatsapp.com/")
        return "Opening WhatsApp 💬"

    elif intent == "gmail":
        webbrowser.open("https://mail.google.com/")
        return "Opening Gmail 📧"

    elif intent == "google":
        webbrowser.open("https://www.google.com/")
        return "Opening Google 🔍"

    elif intent == "facebook":
        webbrowser.open("https://www.facebook.com/")
        return "Opening Facebook 📘"

    elif intent == "instagram":
        webbrowser.open("https://www.instagram.com/")
        return "Opening Instagram 📷"

    elif intent == "twitter":
        webbrowser.open("https://twitter.com/")
        return "Opening Twitter 🐦"

    elif intent == "netflix":
        webbrowser.open("https://www.netflix.com/")
        return "Opening Netflix 🎬"

    elif intent == "spotify":
        webbrowser.open("https://open.spotify.com/")
        return "Opening Spotify 🎵"

    elif intent == "github":
        webbrowser.open("https://github.com/")
        return "Opening GitHub 💻"

    elif intent == "stackoverflow":
        webbrowser.open("https://stackoverflow.com/")
        return "Opening Stack Overflow 💡"

    elif intent == "calculator":
        return open_calculator()

    elif intent == "notepad":
        return open_notepad()

    elif intent == "file_explorer":
        return open_file_explorer()

    elif intent == "time":
        now = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {now}."

    elif intent == "date":
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."

    else:
        return "Sorry, I can't perform that action yet."

def open_calculator():
    """Opens the system calculator"""
    try:
        if platform.system() == "Windows":
            os.system("calc")
            return "Opening Calculator 🧮"
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-a", "Calculator"])
            return "Opening Calculator 🧮"
        else:  # Linux
            subprocess.run(["gnome-calculator"])
            return "Opening Calculator 🧮"
    except:
        return "Could not open calculator"

def open_notepad():
    """Opens the system notepad/text editor"""
    try:
        if platform.system() == "Windows":
            os.system("notepad")
            return "Opening Notepad 📝"
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-a", "TextEdit"])
            return "Opening TextEdit 📝"
        else:  # Linux
            subprocess.run(["gedit"])
            return "Opening Text Editor 📝"
    except:
        return "Could not open text editor"

def open_file_explorer():
    """Opens the system file explorer"""
    try:
        if platform.system() == "Windows":
            os.system("explorer")
            return "Opening File Explorer 📁"
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "."])
            return "Opening Finder 📁"
        else:  # Linux
            subprocess.run(["nautilus"])
            return "Opening File Manager 📁"
    except:
        return "Could not open file explorer"

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
