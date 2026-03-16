import requests

SOURCE = "probate"


def fetch_probate_properties():

    url = "https://api.probateleads.com/properties"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    deals = []

    for item in data.get("data", []):

        deals.append({
            "address": item.get("address"),
            "city": item.get("city"),
            "owner": item.get("owner_name"),
            "source": SOURCE
        })

    return deals


def run():
    deals = fetch_probate_properties()
    print("Probate deals:", deals)
