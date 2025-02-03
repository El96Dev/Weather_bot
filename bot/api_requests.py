import os
from dotenv import load_dotenv
import requests


load_dotenv()
API_TOKEN = os.environ.get("OPEN_WEATHER_TOKEN")


def get_city_coords(city: str) -> dict:
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_TOKEN}"
    response = requests.get(url)
    return response


def get_city_by_coordinates(latitude: str, longitude: str) -> str:
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit=1&appid={API_TOKEN}"
    response = requests.get(url)
    city_data = response[0]
    city = city_data["name"] + ", " + city_data["country"]
    return city


def get_current_weather(latitude: str, longitude: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_TOKEN}"
    response = requests.get(url)
    return response


def get_weather_forecast(latitude: str, longitude: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API_TOKEN}"
    response = requests.get(url)
    return response


def get_air_polution(latitude: str, longitude: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={API_TOKEN}"
    response = requests.get(url)
    return response
