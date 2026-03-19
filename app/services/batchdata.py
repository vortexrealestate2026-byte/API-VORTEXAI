"""
BatchData API integration for pulling motivated seller leads.
Docs: https://batchdata.com/docs
"""
import logging
from typing import Optional

import requests
from sqlalchemy.orm import Session

from app.config import settings
from app.models.lead import Lead

logger = logging.getLogger("vortex.batchdata")

BATCHDATA_BASE_URL = "https://api.batchdata.com/api/v1"


class BatchDataService:
    def __init__(self):
        self.token = settings.BATCHDATA_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _search(self, filters: dict, limit: int = 100) -> list:
        url = f"{BATCHDATA_BASE_URL}/property/search"
        payload = {
            "requests": [
                {
                    "filters": filters,
                    "size": limit,
                    "fields": [
                        "propertyInfo.address",
                        "propertyInfo.city",
                        "propertyInfo.state",
                        "propertyInfo.zip",
                        "ownerInfo.owner1FirstName",
                        "ownerInfo.owner1LastName",
                        "ownerInfo.mobilePhone",
                        "assessmentInfo.estimatedEquity",
                        "propertyId",
                    ],
                }
            ]
        }
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [{}])[0].get("propertyResults", {}).get("results", [])
        except requests.RequestException as exc:
            logger.error(f"BatchData API error: {exc}")
            return []

    def fetch_pre_foreclosure_leads(self, state: str = "US", limit: int = 100) -> list:
        filters = {"preForeclosure": {"isPreForeclosure": True}}
        if state != "US":
            filters["location"] = {"state": state}
        results = self._search(filters, limit)
        return [dict(r, distress_type="pre_foreclosure") for r in results]

    def fetch_absentee_owner_leads(self, state: str = "US", limit: int = 100) -> list:
        filters = {"ownerInfo": {"isAbsenteeOwner": True}}
        if state != "US":
            filters["location"] = {"state": state}
        results = self._search(filters, limit)
        return [dict(r, distress_type="absentee_owner") for r in results]

    def fetch_tax_lien_leads(self, state: str = "US", limit: int = 100) -> list:
        filters = {"taxInfo": {"hasTaxLien": True}}
        if state != "US":
            filters["location"] = {"state": state}
        results = self._search(filters, limit)
        return [dict(r, distress_type="tax_lien") for r in results]

    def _parse_lead(self, raw: dict, distress_type: str) -> Optional[dict]:
        prop = raw.get("propertyInfo", {})
        owner = raw.get("ownerInfo", {})
        assessment = raw.get("assessmentInfo", {})
        property_id = raw.get("propertyId")
        address = prop.get("address")
        city = prop.get("city")
        state = prop.get("state")
        zip_code = prop.get("zip")
        if not all([property_id, address, city, state, zip_code]):
            return None
        owner_name = " ".join(
            filter(None, [owner.get("owner1FirstName"), owner.get("owner1LastName")])
        ) or None
        return {
            "batchdata_id": str(property_id),
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "owner_name": owner_name,
            "phone": owner.get("mobilePhone"),
            "estimated_equity": assessment.get("estimatedEquity"),
            "distress_type": distress_type,
        }

    def ingest_leads(self, db: Session) -> int:
        all_raw = []
        for fetch_fn, distress_type in [
            (self.fetch_pre_foreclosure_leads, "pre_foreclosure"),
            (self.fetch_absentee_owner_leads, "absentee_owner"),
            (self.fetch_tax_lien_leads, "tax_lien"),
        ]:
            try:
                raw_leads = fetch_fn()
                for raw in raw_leads:
                    parsed = self._parse_lead(raw, distress_type)
                    if parsed:
                        all_raw.append(parsed)
            except Exception as exc:
                logger.error(f"Error fetching {distress_type} leads: {exc}")

        inserted = 0
        for lead_data in all_raw:
            batchdata_id = lead_data.get("batchdata_id")
            if batchdata_id:
                existing = db.query(Lead).filter(Lead.batchdata_id == batchdata_id).first()
                if existing:
                    continue
            lead = Lead(**lead_data)
            db.add(lead)
            inserted += 1

        try:
            db.commit()
            logger.info(f"BatchData ingest complete: {inserted} new leads inserted")
        except Exception as exc:
            logger.error(f"DB commit error during lead ingest: {exc}")
            db.rollback()
            inserted = 0

        return inserted
