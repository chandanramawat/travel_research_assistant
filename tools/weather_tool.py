# tools/weather_tool.py
import requests
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """
    Get current weather for a city.
    Use this when user asks about weather at any destination.
    
    Args:
        city: Name of the city like Jaipur or Delhi
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")

    # ✅ API key validate karo
    if not api_key or api_key.startswith("http"):
        return "Error: OpenWeather API key not configured correctly."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        # ✅ API error check karo
        if data.get("cod") != 200:
            return f"Weather error: {data.get('message', 'Unknown error')} for city '{city}'"

        return (
            f"Weather in {data['name']}:\n"
            f"Condition   : {data['weather'][0]['description']}\n"
            f"Temperature : {data['main']['temp']}°C\n"
            f"Humidity    : {data['main']['humidity']}%\n"
        )

    except requests.exceptions.Timeout:
        return f"Weather service timeout for '{city}'"
    except Exception as e:
        return f"Error fetching weather for '{city}': {e}"