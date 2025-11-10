# actions/weather_api.py
import requests

def get_weather(city="Mangalore"):
    """
    Fetches current weather for a given city using the Open-Meteo API (no API key required).
    Uses latitude and longitude fetched via Open-Meteo's geocoding API.
    """
    try:
        # Step 1: Get latitude & longitude from the city name
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=5).json()

        if "results" not in geo_response or len(geo_response["results"]) == 0:
            return f"Couldn't find location for '{city}'."

        lat = geo_response["results"][0]["latitude"]
        lon = geo_response["results"][0]["longitude"]
        name = geo_response["results"][0]["name"]
        country = geo_response["results"][0].get("country", "")

        # Step 2: Fetch current weather using the coordinates
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&timezone=auto"
        )
        weather_response = requests.get(weather_url, timeout=5).json()
        current = weather_response.get("current", {})

        if not current:
            return f"Couldn't fetch weather for '{city}'."

        temp = current.get("temperature_2m", "N/A")
        code = current.get("weather_code", 0)

        # Map basic weather codes to descriptions
        WEATHER_CODES = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm",
        }

        desc = WEATHER_CODES.get(code, "Unknown conditions")

        return f"Current weather in {name}, {country}: {temp}°C, {desc.lower()}."

    except Exception as e:
        return f"Couldn't fetch weather for {city}. ({e})"

