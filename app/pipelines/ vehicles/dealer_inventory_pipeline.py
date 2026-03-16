import requests

DEALER_API = "https://api.yourdealer.com/inventory"


def fetch_dealer_inventory():
    response = requests.get(DEALER_API)

    if response.status_code != 200:
        print("Failed to fetch inventory")
        return []

    data = response.json()

    vehicles = []

    for car in data:
        vehicles.append({
            "title": car["make"] + " " + car["model"],
            "price": car["price"],
            "year": car["year"],
            "source": "dealer_inventory"
        })

    return vehicles


def run():
    vehicles = fetch_dealer_inventory()
    print("Dealer vehicles:", vehicles)
