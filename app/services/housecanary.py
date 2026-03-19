"""
HouseCanary API for property comps, ARV, and valuation.
Docs: https://api-docs.housecanary.com
"""
import logging
from decimal import Decimal
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from app.config import settings

logger = logging.getLogger("vortex.housecanary")

HOUSECANARY_BASE_URL = "https://api.housecanary.com/v2"
ESTIMATED_REPAIRS = Decimal("30000")
OFFER_PERCENTAGE = Decimal("0.70")


class HouseCanaryService:
    def __init__(self):
        self.auth = HTTPBasicAuth(settings.HOUSECANARY_API_KEY, settings.HOUSECANARY_API_SECRET)

    def get_value_report(self, address: str, zipcode: str) -> Optional[dict]:
        url = f"{HOUSECANARY_BASE_URL}/property/value_report"
        params = {"address": address, "zipcode": zipcode}
        try:
            resp = requests.get(url, params=params, auth=self.auth, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            logger.error(f"HouseCanary value_report error for {address} {zipcode}: {exc}")
            return None

    def get_comps(self, address: str, zipcode: str, num_comps: int = 5) -> list:
        url = f"{HOUSECANARY_BASE_URL}/property/sales_history"
        params = {"address": address, "zipcode": zipcode, "num_comps": num_comps}
        try:
            resp = requests.get(url, params=params, auth=self.auth, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            comps_raw = (
                data.get("property/sales_history", {})
                .get("result", {})
                .get("comps", [])
            )
            comps = []
            for c in comps_raw:
                comps.append(
                    {
                        "address": c.get("address", {}).get("full_address", ""),
                        "sale_price": c.get("price"),
                        "sqft": c.get("gross_living_area"),
                        "distance_miles": c.get("distance"),
                        "sale_date": c.get("sale_date"),
                    }
                )
            return comps
        except requests.RequestException as exc:
            logger.error(f"HouseCanary comps error for {address} {zipcode}: {exc}")
            return []

    def analyze_deal(self, address: str, zipcode: str) -> dict:
        arv = None
        comps = []

        report = self.get_value_report(address, zipcode)
        if report:
            value_data = (
                report.get("property/value_report", {})
                .get("result", {})
                .get("value", {})
            )
            price = value_data.get("price_upr") or value_data.get("price_mean")
            if price:
                arv = Decimal(str(price))

        comps = self.get_comps(address, zipcode)

        suggested_offer = None
        if arv is not None:
            suggested_offer = (arv * OFFER_PERCENTAGE) - ESTIMATED_REPAIRS
            if suggested_offer < 0:
                suggested_offer = Decimal("0")

        return {
            "arv": arv,
            "comps": comps,
            "suggested_offer": suggested_offer,
            "estimated_repairs": ESTIMATED_REPAIRS,
            "notes": f"Offer calculated as 70% ARV minus ${ESTIMATED_REPAIRS:,.0f} estimated repairs.",
        }
