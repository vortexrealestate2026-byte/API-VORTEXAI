import requests

SOURCE = "tax_delinquent"


def fetch_tax_delinquent():

    url = "https://api.taxdata.com/delinquent"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()

    deals = []

    for item in data.get("properties", []):

        deals.append({
            "address": item.get("address"),
            "city": item.get("city"),
            "tax_due": item.get("amount_due"),
            "source": SOURCE
        })

    return deals


def run():
    deals = fetch_tax_delinquent()
    print("Tax delinquent:", deals)
