import requests
from bs4 import BeautifulSoup

SOURCE = "facebook_marketplace"


def fetch_marketplace(city="Dallas"):
    url = f"https://www.facebook.com/marketplace/{city}/propertyforsale"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    listings = []

    items = soup.select("a[href*='/marketplace/item']")

    for item in items[:20]:
        title = item.text.strip()

        listings.append({
            "title": title,
            "city": city,
            "source": SOURCE
        })

    return listings


def run():
    deals = fetch_marketplace()
    print("Marketplace deals:", deals)
