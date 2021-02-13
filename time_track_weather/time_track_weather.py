import sys
sys.path.append("lib")
# pi only: from waveshare_epd import epd4in2_V2
import os
from datetime import datetime
import time
import traceback
import telnetlib
import requests, json
from io import BytesIO
import csv

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
icondir = os.path.join(picdir, "icon")
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "font")

API_KEY = "13cd0998435bbe45bf1c548c70384176"
city = "Chicago"
LATITUDE = "48.137154"
LONGITUDE = "11.576124"

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units={'imperial'}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return body

def get_weather_short():
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units={'imperial'}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return {
        "current_temp": body["current"]["temp"],
        "current_conditions": ", ".join(
            [condition["main"] for condition in body["current"]["weather"]]
        ),
        "forecast": [(day["temp"]["max"], day["temp"]["min"]) for day in body["daily"]][
            :3
        ],  # > [(279.4, 273.15), (279.4, 273.15)]
    }

def get_weather_city():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={'imperial'}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return body
        
def get_now_playing():
    url = f"http://192.168.178.167:81/api/track/metadata"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return body

def get_now_playing_short():
    url = f"http://192.168.178.167:81/api/track/metadata"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return (
        body['title'],
        body['artist']
    )
