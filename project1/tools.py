from agents.tool import function_tool
import requests


# Get Weather
@function_tool
async def get_weather(city: str):
    API_KEY = '42743ea5cb7b455ea9e63937242909'
    base_url = f'http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}'
    try:
        respone = requests.get(base_url)
        respone.raise_for_status()
        data = respone.json()

        location = data['location']['name']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        return (f"{location} weather is: {temp_c}°C, {condition},"
                f"Humidity: {humidity}%, Wind Speed: {wind_kph}kph")
    
    except Exception as e:
        return f"Data n ot fetch: {e}"
    