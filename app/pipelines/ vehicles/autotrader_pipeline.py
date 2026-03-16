import requests
from bs4 import BeautifulSoup

SOURCE = "autotrader"


def fetch_autotrader_listings(city="Dallas"):
    url = f"https://www.autotrader.com/cars-for-sale/all-cars/{city}"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    vehicles = []

    listings = soup.select(".inventory-listing")

    for item in listings[:10]:
        title = item.select_one(".inventory-listing-header").text.strip()
        price = item.select_one(".first-price").text.strip()

        vehicles.append({
            "title": title,
            "price": price,
            "source": SOURCE,
            "city": city
        })

    return vehicles


def run():
    vehicles = fetch_autotrader_listings()
    print("Autotrader vehicles:", vehicles)
