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
CITY = "Munich"
STATE = ""
COUNTRY = "DE"

def get_city_geo(CITY,STATE,COUNTRY):
    url = f"https://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={1}&appid={API_KEY}}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    return body
