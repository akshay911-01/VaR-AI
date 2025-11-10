# actions/action_router.py
import webbrowser
import datetime
import requests
import os
import subprocess
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import nltk
nltk.download('punkt_tab')

def handle_intent(intent, raw_text=None):
    """
    Handles app or command-based intents.
    """
    if intent == "weather":
        return get_weather()

    elif intent == "youtube":
        webbrowser.open("https://www.youtube.com/")
        return "Opening YouTube 🎵"
    
    elif intent == "music":
        webbrowser.open("https://open.spotify.com/")
        return "Opening Spotify 🎵"

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

    elif intent == "compose_email":
        return compose_email(raw_text)

    elif intent == "send_email":
        return send_email(raw_text)

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

import requests
from actions.weather_api import get_weather

# def get_weather(city="Bangalore"):
#     """
#     Fetches current weather for a given city using the Open-Meteo API (no API key needed).
#     """
#     try:
#         # Step 1: Get latitude and longitude for the city
#         geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
#         geo_response = requests.get(geo_url, timeout=5).json()

#         if "results" not in geo_response or not geo_response["results"]:
#             return f"Couldn't find location for '{city}'."

#         lat = geo_response["results"][0]["latitude"]
#         lon = geo_response["results"][0]["longitude"]
#         name = geo_response["results"][0]["name"]
#         country = geo_response["results"][0].get("country", "")

#         # Step 2: Get current weather data
#         weather_url = (
#             f"https://api.open-meteo.com/v1/forecast?"
#             f"latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&timezone=auto"
#         )
#         weather_response = requests.get(weather_url, timeout=5).json()
#         current = weather_response.get("current", {})

#         if not current:
#             return f"Couldn't fetch weather for '{city}'."

#         temp = current.get("temperature_2m", "N/A")
#         code = current.get("weather_code", 0)

#         # Step 3: Map weather code to description
#         WEATHER_CODES = {
#             0: "Clear sky",
#             1: "Mainly clear",
#             2: "Partly cloudy",
#             3: "Overcast",
#             45: "Foggy",
#             48: "Depositing rime fog",
#             51: "Light drizzle",
#             61: "Slight rain",
#             63: "Moderate rain",
#             65: "Heavy rain",
#             71: "Slight snow",
#             73: "Moderate snow",
#             75: "Heavy snow",
#             95: "Thunderstorm",
#         }

#         desc = WEATHER_CODES.get(code, "Unknown conditions")

#         return f"The weather in {name}, {country} is {desc.lower()} with a temperature of {temp}°C."

#     except Exception as e:
#         return f"Error fetching weather details for {city}: {e}"


def compose_email(user_input):
    """
    Composes an email based on user input and opens email compose.
    """
    try:
        import urllib.parse
        
        # Parse user input for email details
        lines = user_input.split('\n')
        to_email = ""
        subject = "Email from AI Assistant"
        body = user_input
        
        # Extract recipient, subject, and body from input
        for line in lines:
            line_lower = line.lower().strip()
            if line_lower.startswith("to:") or line_lower.startswith("send to:"):
                to_email = line.split(":")[-1].strip()
            elif line_lower.startswith("subject:"):
                subject = line.split(":")[-1].strip()
            elif line_lower.startswith("body:") or line_lower.startswith("message:"):
                body = line.split(":")[-1].strip()
        
        # If no specific body found, use the whole input as body
        if body == user_input and not any(line.lower().startswith(("to:", "subject:", "body:", "message:")) for line in lines):
            body = f"Hello,\n\n{user_input}\n\nBest regards,\nAI Assistant"
        
        # URL encode the email content
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(body)
        to_encoded = urllib.parse.quote(to_email)
        
        # Try different email providers
        email_urls = [
            # Gmail
            f"https://mail.google.com/mail/?view=cm&fs=1&to={to_encoded}&su={subject_encoded}&body={body_encoded}",
            # Outlook
            f"https://outlook.live.com/mail/0/deeplink/compose?to={to_encoded}&subject={subject_encoded}&body={body_encoded}",
            # Yahoo
            f"https://compose.mail.yahoo.com/?to={to_encoded}&subject={subject_encoded}&body={body_encoded}"
        ]
        
        # Open Gmail first (most common)
        webbrowser.open(email_urls[0])
        
        return f"Opening email compose with your message to {to_email or 'recipient'}: '{body[:50]}{'...' if len(body) > 50 else ''}' 📧"
    
    except Exception as e:
        return f"Error composing email: {str(e)}"

def send_email(user_input):
    """
    Sends an email using SMTP (requires email configuration).
    """
    try:
        # This is a template - you'll need to configure your email settings
        # For security, store email credentials in environment variables
        
        # Example configuration (replace with your actual settings)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("EMAIL_ADDRESS", "your-email@gmail.com")
        sender_password = os.getenv("EMAIL_PASSWORD", "your-app-password")
        
        # Parse user input for email details
        # This is a simple parser - you can make it more sophisticated
        lines = user_input.split('\n')
        to_email = "recipient@example.com"  # Default recipient
        subject = "Email from AI Assistant"
        body = user_input
        
        # Try to extract recipient from input
        for line in lines:
            if "to:" in line.lower() or "send to:" in line.lower():
                to_email = line.split(":")[-1].strip()
            elif "subject:" in line.lower():
                subject = line.split(":")[-1].strip()
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        return f"Email sent successfully to {to_email} with subject: '{subject}' 📧"
    
    except Exception as e:
        return f"Error sending email: {str(e)}. Please check your email configuration."

def draft_email(user_input):
    """
    Creates a draft email and saves it locally.
    """
    try:
        # Create email draft
        draft = {
            "timestamp": datetime.datetime.now().isoformat(),
            "content": user_input,
            "subject": "Draft Email",
            "to": "recipient@example.com"
        }
        
        # Save draft to file
        draft_file = "email_draft.json"
        with open(draft_file, 'w') as f:
            json.dump(draft, f, indent=2)
        
        return f"Email draft saved! You can find it in {draft_file} 📝"
    
    except Exception as e:
        return f"Error creating draft: {str(e)}"
