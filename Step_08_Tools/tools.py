import os
from dotenv import load_dotenv, find_dotenv
import requests
from agents import function_tool

load_dotenv(find_dotenv())
weather_api_key = os.getenv("WEATHER_API_KEY")

@function_tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""

    result = requests.get(url=f"http://api.weatherapi.com/v1//current.json?key={weather_api_key}&q={location}")
    data = result.json()

    return f"The current weather in {data['location']['name']} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
