import requests
from bs4 import BeautifulSoup

SOURCE = "redfin"


def fetch_redfin(city="Dallas"):

    url = f"https://www.redfin.com/city/{city}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    items = soup.select(".homecard")

    for item in items[:20]:

        listings.append({
            "title": item.text.strip(),
            "city": city,
            "source": SOURCE
        })

    return listings


def run():
    deals = fetch_redfin()
    print("Redfin deals:", deals)
