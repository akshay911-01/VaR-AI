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
    
    elif intent == "name":
        return "I'm VIRAI — your advanced, intelligent, and efficient virtual assistant powered by the Mistral 7B model 💫"

    elif intent == "greeting":
        return "Hello there ✨ I’m VIRAI — your virtual assistant, ready to help. How are you today?"

    elif intent == "capabilities":
        return (
        "I can help you manage tasks, check the weather, compose emails, summarize text, "
        "and assist with technical or creative work. What would you like me to do next?"
    )


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


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os
import json
import datetime

def extract_email_and_body(user_input):
    """
    Extracts email address, subject, and body text from user input.
    Handles both structured input (to:, subject:, body:) and natural text.
    """
    lines = user_input.split("\n")
    to_email = None
    subject = ""
    body_lines = []

    # Try to find a valid email address anywhere in the text
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_input)
    if email_match:
        to_email = email_match.group(0)

    # Look for structured fields if present
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower.startswith(("to:", "send to:")):
            to_email = line.split(":", 1)[-1].strip()
        elif line_lower.startswith("subject:"):
            subject = line.split(":", 1)[-1].strip()
        elif line_lower.startswith(("body:", "message:")):
            body_lines.append(line.split(":", 1)[-1].strip())
        else:
            # Treat non-structured lines as part of the body if not 'to:' or 'subject:'
            if not any(line_lower.startswith(x) for x in ("to:", "subject:", "body:", "message:")):
                body_lines.append(line.strip())

    body = "\n".join([line for line in body_lines if line])
    if not body:
        body = "No message content provided."

    return to_email, subject or "Email from VIRAI", body


def send_email(user_input):
    """
    Sends an email using SMTP to the address mentioned in the user input.
    Requires EMAIL_ADDRESS and EMAIL_PASSWORD set as environment variables.
    """
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("EMAIL_ADDRESS", "your-email@gmail.com")
        sender_password = os.getenv("EMAIL_PASSWORD", "your-app-password")

        to_email, subject, body = extract_email_and_body(user_input)

        if not to_email:
            return "Couldn't find a valid email address in your message."

        # Create email message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send via Gmail SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return f"Email sent successfully to {to_email} with subject: '{subject}' 📧"

    except Exception as e:
        return f"Error sending email: {str(e)}. Please check your email configuration."


def draft_email(user_input):
    """
    Creates an email draft from user input and saves it locally as JSON.
    """
    try:
        to_email, subject, body = extract_email_and_body(user_input)
        draft = {
            "timestamp": datetime.datetime.now().isoformat(),
            "to": to_email or "recipient@example.com",
            "subject": subject,
            "body": body,
        }

        draft_file = "email_draft.json"
        with open(draft_file, "w") as f:
            json.dump(draft, f, indent=2)

        return f"Email draft saved! You can find it in {draft_file} 📝"

    except Exception as e:
        return f"Error creating draft: {str(e)}"

import webbrowser
import urllib.parse
import re

def compose_email(user_input):
    """
    Extracts email and message from user input and opens Gmail compose window.
    """
    try:
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', user_input)
        if email_match:
            to_email = email_match.group(0)
        else:
            return "Couldn't find a valid email address in your message."

        # Extract message (everything after 'say' or after the email)
        message = ""
        if "say" in user_input.lower():
            message = user_input.split("say", 1)[-1].strip(" \"'")
        elif "message" in user_input.lower():
            message = user_input.split("message", 1)[-1].strip(" \"'")
        else:
            # fallback: take entire text after email as message
            parts = user_input.split(to_email)
            if len(parts) > 1:
                message = parts[1].strip()
            else:
                message = "Hello!"

        # Prepare Gmail compose URL
        subject = "Enter subject here"
        to_encoded = urllib.parse.quote(to_email)
        subject_encoded = urllib.parse.quote(subject)
        body_encoded = urllib.parse.quote(message)

        gmail_url = (
            f"https://mail.google.com/mail/?view=cm&fs=1"
            f"&to={to_encoded}&su={subject_encoded}&body={body_encoded}"
        )

        webbrowser.open(gmail_url)
        return f"Opening Gmail compose for {to_email} with message: “{message}” 📧"

    except Exception as e:
        return f"Error composing email: {str(e)}"
