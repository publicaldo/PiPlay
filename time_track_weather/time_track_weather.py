import sys
sys.path.append("lib")
# from waveshare_epd import epd4in2_V2 # pi only:
import os
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

def get_date():
    now = datetime.now()
    current_date = now.strftime("%a, %b %d")
    return(current_date)

def get_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    return(current_time)

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units={'imperial'}"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body = response.json()
# this text works, but is a bit clumsy?
    current_temp = round(body["current"]["temp"])
    current_conditions = [condition["main"] for condition in body["current"]["weather"]][0] # I'd like to return a link to the icon?  or specific font character for font.
    hi_today = [round(day["temp"]["max"]) for day in body["daily"]][0]
    lo_today = [round(day["temp"]["min"]) for day in body["daily"]][0]
    hi_tomorrow = [round(day["temp"]["max"]) for day in body["daily"]][1]
    lo_tomorrow = [round(day["temp"]["min"]) for day in body["daily"]][1]
#     conditions_tomorrow = [condition["main"] for condition in body["daily"]][1:2] # don't know how to get tomorrow's conditions
    return current_temp, current_conditions, hi_today, lo_today, hi_tomorrow, lo_tomorrow

def get_now_playing():
    url = f"http://hifiberry.local:81/api/track/metadata"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body=response.json()
    title = body['title']
    artist = body['artist']
    releaseDate = body['releaseDate']
#     if releaseDate=none then make it ""
#     if releaseDate == none:
#         releaseDate = ""
    playerName = body['playerName']
    if playerName == "mpd":
        playerName = "Radio"
    if playerName == "ShairportSync":
        playerName = "AirPlay"
# THere's got to be a case or list translate for this
# also - if Radio, can we get the channel name?
# - maybe brute force it from the url
    return title, artist, releaseDate, playerName

#Daily calendar loop
#    get formatted date and timne
current_date=get_date() 
current_time=get_time() # at this time / in this loop for this development exercise
#    update date section
# print(current_date) # commented for this dev exercise
print(current_date, current_time, sep=' - ') # separate time into minute loop after dev
print()

#1 minute time loop
#    get formatted time
#    update time section
# print(current_time)

#15 minute weather loop#
#    Get weather
(current_temp, current_conditions, hi_today, lo_today, hi_tomorrow, lo_tomorrow)=get_weather()
#    update weather section
print("Weather")
print("Current: ", current_temp, "and", current_conditions)
print("Today: high", hi_today, "low", lo_today)
print("Tomorrow: high", hi_tomorrow, "low", lo_tomorrow) 

#5 second now playing loop
#    get now playing
(title, artist, releaseDate, playerName)=get_now_playing()
#    check if new - artist, title should be enough
# if yes, update song section
print()
print(playerName)
print(title, artist, releaseDate, sep=' | ')
# if(releaseDate') = "none", releaseDate=""

# example timing and control loop from Pythn turtle clock example
#def tick():
#    t = datetime.today()
#    second = t.second + t.microsecond*0.000001
#    minute = t.minute + second/60.0
#    hour = t.hour + minute/60.0
#    try:
#        tracer(False)  # Terminator can occur here
#        writer.clear()
#        writer.home()      
# 
#def main():
#    tracer(False)
#    setup()
#    tracer(True)
#    tick()
#    return "EVENTLOOP"
#
#if __name__ == "__main__":
#    mode("logo")
#    msg = main()
#    print(msg)
#    mainloop()


