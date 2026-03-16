import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

SOURCE = "google_ads"


def fetch_google_leads():

    url = "https://googleads.googleapis.com/v14/customers"

    headers = {
        "Authorization": f"Bearer {GOOGLE_API_KEY}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Google Ads API error")
        return []

    data = response.json()

    leads = []

    for item in data.get("results", []):

        leads.append({
            "campaign": item.get("campaign"),
            "keyword": item.get("keyword"),
            "city": item.get("location"),
            "source": SOURCE
        })

    return leads


def run():
    leads = fetch_google_leads()
    print("Google leads:", leads)
