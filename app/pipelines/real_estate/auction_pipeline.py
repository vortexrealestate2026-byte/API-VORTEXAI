import requests

SOURCE = "auction"


def fetch_auction_properties(city="Dallas"):

    url = f"https://api.auctiondata.com/properties?city={city}"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    deals = []

    for item in data.get("results", []):

        deals.append({
            "title": item.get("address"),
            "city": city,
            "price": item.get("price"),
            "source": SOURCE
        })

    return deals


def run():
    deals = fetch_auction_properties()
    print("Auction deals:", deals)
