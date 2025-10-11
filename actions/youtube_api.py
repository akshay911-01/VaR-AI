# actions/youtube_api.py
import pywhatkit as pwk

def play_on_youtube(query):
    try:
        pwk.playonyt(query)
        return f"Playing {query} on YouTube."
    except Exception as e:
        return f"Failed to play {query}: {e}"
