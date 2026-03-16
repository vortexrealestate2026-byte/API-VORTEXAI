import requests
import logging
from datetime import datetime

SOURCE = "custom_pipeline_20"

# Example external source
DATA_SOURCE = "https://api.example.com/deals"


def fetch_data():

    try:

        response = requests.get(DATA_SOURCE, timeout=10)

        if response.status_code != 200:
            logging.warning("Custom pipeline failed")
            return []

        data = response.json()

        results = []

        for item in data.get("results", []):

            results.append({
                "title": item.get("title"),
                "address": item.get("address"),
                "city": item.get("city"),
                "price": item.get("price"),
                "source": SOURCE,
                "created_at": datetime.utcnow().isoformat()
            })

        return results

    except Exception as e:
        logging.error(f"Pipeline error: {e}")
        return []


def run():

    logging.info("Running custom pipeline 20")

    deals = fetch_data()

    logging.info(f"Deals collected: {len(deals)}")

    for deal in deals:
        print(deal)

    return deals
