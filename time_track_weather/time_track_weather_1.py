import sys
sys.path.append("lib")
# from waveshare_epd import epd4in2_V2 # pi only:
import os
import time
from datetime import datetime
import requests

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pic")
icondir = os.path.join(picdir, "icon")
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "font")

API_KEY = "13cd0998435bbe45bf1c548c70384176"
CITY = "Munich"
STATE = ""
COUNTRY = "DE"
LATITUDE = "48.137154"
LONGITUDE = "11.576124"
oldMinute = ""
oldHour = ""
oldDate = ""
oldTitle = ""


def get_time():
    now = datetime.now()
    currentTime = now.strftime("%I:%M %p")
    currentMinute = now.strftime("%M")
    currentHour = now.strftime("%I")
    currentDate = now.strftime("%a, %b %d")
    return currentTime, currentMinute, currentHour, currentDate

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units={'imperial'}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
    temp = round(body["current"]["temp"])
    conditions = [condition["main"] for condition in body["current"]["weather"]][0] # I'd like to return a link to the icon?  or specific font character for font.
    hiToday = [round(day["temp"]["max"]) for day in body["daily"]][0]
    loToday = [round(day["temp"]["min"]) for day in body["daily"]][0]
    hiTomorrow = [round(day["temp"]["max"]) for day in body["daily"]][1]
    loTomorrow = [round(day["temp"]["min"]) for day in body["daily"]][1]
    return temp, conditions, hiToday, loToday, hiTomorrow, loTomorrow

def get_now_playing():
    url = f"http://hifiberry.local:81/api/track/metadata"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body=response.json()
    title = body['title']
    artist = body['artist']
    releaseDate = body['releaseDate']
    playerName = body['playerName']
    if playerName == "mpd": # There's got to be a case or list translate for this
        playerName = "Radio" # also - if Radio, can we get the channel name?  Brute from url?
    if playerName == "ShairportSync":
        playerName = "AirPlay"
    return title, artist, releaseDate, playerName

while True:
    time.sleep(1)
    (title, artist, releaseDate, playerName) = get_now_playing()
    (currentTime, currentMinute, currentHour, currentDate) = get_time()
    (temp, conditions, hiToday, loToday, hiTomorrow, loTomorrow) = get_weather()

    if not currentDate == oldDate:
        print(currentDate)
        oldDate = currentDate
        
    if not currentMinute == oldMinute:
        print(currentTime)
        oldMinute = currentMinute
      
    if not title == oldTitle:
        print()
        print(playerName)
        print(title, artist, releaseDate, sep=' | ')
        print()
        oldTitle = title
      
    if not currentHour == oldHour:
        print("Weather")
        print("Current: ", temp, "and", conditions)
        print("Today: high", hiToday, "low", loToday)
        print("Tomorrow: high", hiTomorrow, "low", loTomorrow)
        print()
        oldHour = currentHour

      
    
  



