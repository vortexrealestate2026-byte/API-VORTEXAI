import requests

TRADEIN_API = "https://api.yourplatform.com/tradein-leads"


def fetch_tradein_leads():
    response = requests.get(TRADEIN_API)

    if response.status_code != 200:
        return []

    leads = response.json()

    tradeins = []

    for lead in leads:
        tradeins.append({
            "customer_name": lead["name"],
            "vehicle": lead["vehicle"],
            "year": lead["year"],
            "mileage": lead["mileage"],
            "source": "tradein"
        })

    return tradeins


def run():
    tradeins = fetch_tradein_leads()
    print("Trade-in leads:", tradeins)
