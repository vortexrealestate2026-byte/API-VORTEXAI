import requests
import os

ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("FB_AD_ACCOUNT_ID")

SOURCE = "facebook_ads"


def fetch_facebook_leads():

    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/leads"

    params = {
        "access_token": ACCESS_TOKEN
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Facebook API error")
        return []

    data = response.json()

    leads = []

    for lead in data.get("data", []):
        leads.append({
            "name": lead.get("name"),
            "email": lead.get("email"),
            "phone": lead.get("phone"),
            "source": SOURCE
        })

    return leads


def run():
    leads = fetch_facebook_leads()
    print("Facebook leads:", leads)
