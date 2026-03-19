import logging

import requests

from app.config import settings
from app.models.car_lead import CarLead

logger = logging.getLogger("vortex.make_webhook")


class MakeWebhookService:
    def __init__(self):
        self.webhook_url = settings.MAKE_WEBHOOK_URL

    def trigger_car_lead(self, car_lead: CarLead) -> bool:
        if not self.webhook_url:
            logger.warning("MAKE_WEBHOOK_URL is not configured, skipping Make.com trigger")
            return False

        payload = {
            "id": str(car_lead.id),
            "name": car_lead.name,
            "phone": car_lead.phone,
            "email": car_lead.email,
            "province": car_lead.province,
            "income_range": car_lead.income_range,
            "credit_score_range": car_lead.credit_score_range,
            "vehicle_type": car_lead.vehicle_type,
            "status": car_lead.status,
            "created_at": car_lead.created_at.isoformat() if car_lead.created_at else None,
        }

        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=15,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            logger.info(f"Make.com webhook triggered for car lead {car_lead.id}: status={response.status_code}")
            return True
        except requests.RequestException as exc:
            logger.error(f"Make.com webhook error for car lead {car_lead.id}: {exc}")
            return False
