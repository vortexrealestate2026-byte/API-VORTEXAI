import requests
from bs4 import BeautifulSoup

def scrape_properties():

    url = "https://example-realestate-site.com"

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    properties = []

    for listing in soup.select(".listing"):

        properties.append({
            "address": listing.select_one(".address").text,
            "price": listing.select_one(".price").text
        })

    return properties


def get_properties():
    return scrape_properties()
