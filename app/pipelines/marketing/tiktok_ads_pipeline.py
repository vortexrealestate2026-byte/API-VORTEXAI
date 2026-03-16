import requests
import os

ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")
ADVERTISER_ID = os.getenv("TIKTOK_ADVERTISER_ID")

SOURCE = "tiktok_ads"


def fetch_tiktok_leads():

    url = "https://business-api.tiktok.com/open_api/v1.3/lead/get/"

    headers = {
        "Access-Token": ACCESS_TOKEN
    }

    params = {
        "advertiser_id": ADVERTISER_ID
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("TikTok API error")
        return []

    data = response.json()

    leads = []

    for lead in data.get("data", {}).get("leads", []):

        leads.append({
            "name": lead.get("name"),
            "phone": lead.get("phone"),
            "email": lead.get("email"),
            "source": SOURCE
        })

    return leads


def run():
    leads = fetch_tiktok_leads()
    print("TikTok leads:", leads)
