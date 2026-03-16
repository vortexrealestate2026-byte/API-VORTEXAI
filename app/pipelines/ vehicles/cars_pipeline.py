import requests
from bs4 import BeautifulSoup

SOURCE = "cars.com"


def fetch_cars_listings(city="Dallas"):
    url = f"https://www.cars.com/shopping/results/?stock_type=used&list_price_max=&makes[]=&maximum_distance=all&zip=75001"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    vehicles = []

    listings = soup.select(".vehicle-card")

    for item in listings[:10]:
        title = item.select_one(".title").text.strip()
        price = item.select_one(".primary-price").text.strip()

        vehicles.append({
            "title": title,
            "price": price,
            "source": SOURCE,
            "city": city
        })

    return vehicles


def run():
    vehicles = fetch_cars_listings()
    print("Cars.com vehicles:", vehicles)
