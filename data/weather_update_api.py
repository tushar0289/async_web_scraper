from dotenv import load_dotenv
from pprint import pprint
import requests, os


load_dotenv("api_keys.env")
api_key = os.getenv("OPEN_WEATHER_API_KEY").strip()


city = "Dhaka"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    pprint(data)

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    print(f"Success! The weather in {city} is {temp}C with {desc}.")

else:
    print(f"Error {response.status_code}: {response.text}")
