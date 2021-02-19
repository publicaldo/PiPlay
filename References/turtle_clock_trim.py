#!/usr/bin/env python3
# -*- coding: cp1252 -*-
"""
turtle-example-suite
tdemo_clock.py
Modified to include weather and HFB info

Enhanced clock-program, showing date
and time
  ------------------------------------
   Press STOP to exit the program!
  ------------------------------------
"""
import sys
sys.path.append("lib")
## pi only: from waveshare_epd import epd4in2_V2
import os
import requests
from turtle import *
from datetime import datetime

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
icondir = os.path.join(picdir, "icon")
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "font")

API_KEY = "13cd0998435bbe45bf1c548c70384176"
CITY = "Munich"
STAE = ""
Country = "DE"
LATITUDE = "48.137154"
LONGITUDE = "11.576124"
DISPLAY_FONT = "weathericons-regular-webfont"


def setup():
    global writer
    ht()
    writer = Turtle()
    #writer.mode("logo")
    writer.ht()
    writer.pu()
    writer.bk(0)
    
    

def get_date():
    now = datetime.now()
    current_date = now.strftime("%a, %b %d")
    return(current_date)

def get_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    return(current_time)
    
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

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units={'imperial'}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    current_temp = round(body["current"]["temp"])
    current_conditions = [condition["main"] for condition in body["current"]["weather"]]
    hi_today = [round(day["temp"]["max"]) for day in body["daily"]][:1]
    lo_today = [round(day["temp"]["min"]) for day in body["daily"]][:1]
    hi_tomorrow = [round(day["temp"]["max"]) for day in body["daily"]][1:2]
    lo_tomorrow = [round(day["temp"]["max"]) for day in body["daily"]][1:2]
##    conditions_tomorrow = [condition["main"] for condition in body["daily"]][1:2]
    return current_temp, current_conditions, hi_today, lo_today, hi_tomorrow, lo_tomorrow


def tick():
    try:
        tracer(False)  # Terminator can occur here
        writer.clear()
        writer.home()

        
## on song change?
        writer.write(get_now_playing(),
                    align="left", font=(DISPLAY_FONT, 12, "bold"))
        writer.forward(35)
# hourly or quarter-hourly
#         writer.write(get_weather(),
#                     align="left", font=(DISPLAY_FONT, 18, "bold"))
#         writer.forward(35)
## daily
        writer.write(get_date(),
                     align="left", font=(DISPLAY_FONT, 12, "bold"))
        writer.forward(35)
## minutely
        writer.write(get_time(),
                    align="left", font=(DISPLAY_FONT, 12, "bold"))
        writer.forward(35)  

## error / end
        tracer(True)
        ontimer(tick, 20000)
    except Terminator:
        pass  # turtledemo user pressed STOP


def main():
    tracer(False)
    setup()
    tracer(True)
    tick()
    return "EVENTLOOP"

if __name__ == "__main__":
    mode("logo")
    msg = main()
    print(msg)
    mainloop()

