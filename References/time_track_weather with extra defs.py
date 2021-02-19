import sys
sys.path.append("lib")
## pi only: from waveshare_epd import epd4in2_V2
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
CITY = "Munich"
STAE = ""
Country = "DE"
LATITUDE = "48.137154"
LONGITUDE = "11.576124"

def get_weather():
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
            :2
        ],  # > [(279.4, 273.15), (279.4, 273.15)]
    }


def get_now_playing():
    url = f"http://192.168.178.167:81/api/track/metadata"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return (
##      show song and artist in big fonts
        body['title'],
        body['artist'],
##      show icon for player source
        body['playerName']
    )


##Main
##Daily calendar loop
##    update date section
##1 hour weather loop
##    Get weather
print(get_weather())
print()
##    update weather section
##1 minute time loop
##    update time section
##5 second now playing loop
##    if new, update now playing section
print(get_now_playing())
print()


