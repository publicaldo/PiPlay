# HifiBerry complete api
import requests

def get_now_playing():
    url = f"http://hifiberry.local:81/api/track/metadata"
    response = requests.get(url)
    if not response.ok:
        raise Exception(response.json()["message"])
    body=response.json()
    return body

print(get_now_playing())