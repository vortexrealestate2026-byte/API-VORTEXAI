import requests

REFERRAL_API = "https://yourplatform.com/api/referrals"


def fetch_referrals():

    response = requests.get(REFERRAL_API)

    if response.status_code != 200:
        return []

    referrals = response.json()

    deals = []

    for r in referrals:

        deals.append({
            "referrer": r.get("name"),
            "phone": r.get("phone"),
            "deal_address": r.get("address"),
            "city": r.get("city"),
            "price": r.get("price"),
            "source": "referral"
        })

    return deals


def run():
    referrals = fetch_referrals()
    print("Referral deals:", referrals)
