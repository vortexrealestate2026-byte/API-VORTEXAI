import requests
import logging
from datetime import datetime

SOURCE = "wholesale_feed"

WHOLESALE_FEEDS = [
    "https://api.wholesaledeals.com/feed",
    "https://api.investorlistings.com/deals",
    "https://api.offmarketproperties.com/listings"
]


def fetch_feed(url):

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            logging.warning(f"Feed failed: {url}")
            return []

        data = response.json()

        deals = []

        for item in data.get("results", []):

            deal = {
                "title": item.get("title"),
                "address": item.get("address"),
                "city": item.get("city"),
                "state": item.get("state"),
                "price": item.get("price"),
                "arv": item.get("arv"),
                "repair_cost": item.get("repair_cost"),
                "property_type": item.get("property_type"),
                "source": SOURCE,
                "created_at": datetime.utcnow().isoformat()
            }

            deals.append(deal)

        return deals

    except Exception as e:
        logging.error(f"Feed error {url}: {e}")
        return []


def fetch_all_feeds():

    all_deals = []

    for feed in WHOLESALE_FEEDS:

        deals = fetch_feed(feed)

        if deals:
            all_deals.extend(deals)

    return all_deals


def run():

    logging.info("Running wholesale feed pipeline")

    deals = fetch_all_feeds()

    logging.info(f"Deals collected: {len(deals)}")

    for deal in deals:
        print(deal)

    return deals
