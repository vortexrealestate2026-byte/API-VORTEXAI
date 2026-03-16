
import requests

INVESTOR_API = "https://yourplatform.com/api/investors"


def fetch_investors():

    response = requests.get(INVESTOR_API)

    if response.status_code != 200:
        return []

    investors = response.json()

    buyer_list = []

    for investor in investors:

        buyer_list.append({
            "name": investor.get("name"),
            "email": investor.get("email"),
            "phone": investor.get("phone"),
            "city": investor.get("city"),
            "buy_box": investor.get("criteria"),
            "cash_ready": investor.get("cash_ready"),
            "source": "investor_network"
        })

    return buyer_list


def run():
    investors = fetch_investors()
    print("Investor buyers:", investors)
