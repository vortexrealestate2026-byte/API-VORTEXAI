import requests

def get_properties():

    url = "https://api.example.com/properties"
    r = requests.get(url)

    return r.json()
