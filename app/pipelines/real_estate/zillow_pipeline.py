import requests
from bs4 import BeautifulSoup

SOURCE = "zillow"


def fetch_zillow(city="Dallas"):

    url = f"https://www.zillow.com/homes/{city}_rb/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    items = soup.select(".property-card")

    for item in items[:20]:

        listings.append({
            "title": item.text.strip(),
            "city": city,
            "source": SOURCE
        })

    return listings


def run():
    deals = fetch_zillow()
    print("Zillow deals:", deals)
