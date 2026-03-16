import requests

SOURCE = "vacant_property"


def fetch_vacant_properties():

    url = "https://api.vacanthomes.com/list"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    deals = []

    for item in data.get("data", []):

        deals.append({
            "address": item.get("address"),
            "city": item.get("city"),
            "vacant": True,
            "source": SOURCE
        })

    return deals


def run():
    deals = fetch_vacant_properties()
    print("Vacant properties:", deals)
