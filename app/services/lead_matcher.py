import logging
from datetime import datetime

import requests
from sqlalchemy.orm import Session

from app.models.car_lead import CarLead
from app.models.dealer import Dealer
from app.models.lead_delivery import LeadDelivery
from app.services.stripe_service import StripeService

logger = logging.getLogger("vortex.lead_matcher")

CREDIT_SCORE_TO_TIER = {
    "under_550": "under_550",
    "550_599": "550_599",
    "600_649": "600_649",
    "650_699": "650_699",
    "700_749": "700_749",
    "750_plus": "750_plus",
}


def _credit_score_matches_tiers(credit_score_range: str, dealer_tiers: list) -> bool:
    """Check if the lead's credit score range overlaps with any dealer credit tier."""
    if not dealer_tiers:
        return True
    tier_ranges = {
        "under_550": 525,
        "550_599": 574,
        "600_649": 624,
        "650_699": 674,
        "700_749": 724,
        "750_plus": 775,
    }
    lead_score = tier_ranges.get(credit_score_range, 0)
    for tier in dealer_tiers:
        if "-" in tier:
            parts = tier.split("-")
            try:
                low, high = int(parts[0]), int(parts[1])
                if low <= lead_score <= high:
                    return True
            except ValueError:
                pass
        elif "+" in tier:
            try:
                low = int(tier.replace("+", ""))
                if lead_score >= low:
                    return True
            except ValueError:
                pass
        elif tier == credit_score_range:
            return True
    return False


def match_and_deliver_lead(car_lead_id: str, db: Session) -> dict:
    """
    1. Get car lead from DB
    2. Find matching active dealers
    3. Deliver to each eligible dealer
    4. Bill via Stripe
    5. Log results
    """
    car_lead = db.query(CarLead).filter(CarLead.id == car_lead_id).first()
    if not car_lead:
        logger.error(f"lead_matcher: car lead {car_lead_id} not found")
        return {"error": "CarLead not found"}

    dealers = (
        db.query(Dealer)
        .filter(
            Dealer.province == car_lead.province,
            Dealer.is_active == True,
        )
        .all()
    )

    eligible_dealers = []
    for dealer in dealers:
        if dealer.leads_this_month >= dealer.monthly_lead_cap:
            continue
        if dealer.vehicle_types and car_lead.vehicle_type not in dealer.vehicle_types:
            continue
        if dealer.credit_tiers and not _credit_score_matches_tiers(car_lead.credit_score_range, dealer.credit_tiers):
            continue
        eligible_dealers.append(dealer)

    stripe_svc = StripeService()
    delivered = 0
    failed = 0

    for dealer in eligible_dealers:
        response_code = None
        if dealer.crm_webhook_url:
            try:
                resp = requests.post(
                    dealer.crm_webhook_url,
                    json={
                        "lead_id": str(car_lead.id),
                        "name": car_lead.name,
                        "phone": car_lead.phone,
                        "email": car_lead.email,
                        "province": car_lead.province,
                        "income_range": car_lead.income_range,
                        "credit_score_range": car_lead.credit_score_range,
                        "vehicle_type": car_lead.vehicle_type,
                    },
                    timeout=10,
                )
                response_code = resp.status_code
            except requests.RequestException as exc:
                logger.error(f"Webhook delivery failed to dealer {dealer.id}: {exc}")
                response_code = 0
                failed += 1
                continue

        usage_record_id = None
        try:
            usage_record_id = stripe_svc.record_lead_usage(dealer, quantity=1)
        except Exception as exc:
            logger.error(f"Stripe usage record error for dealer {dealer.id}: {exc}")

        delivery = LeadDelivery(
            car_lead_id=car_lead.id,
            dealer_id=dealer.id,
            delivered_at=datetime.utcnow(),
            webhook_response_code=response_code,
            billed=usage_record_id is not None,
            stripe_usage_record_id=usage_record_id,
        )
        db.add(delivery)

        dealer.leads_this_month += 1
        delivered += 1

    if delivered > 0:
        car_lead.status = "delivered"
    elif eligible_dealers:
        car_lead.status = "matched"
    else:
        car_lead.status = "unmatched"

    try:
        db.commit()
    except Exception as exc:
        logger.error(f"DB commit error in lead_matcher: {exc}")
        db.rollback()

    result = {
        "car_lead_id": str(car_lead_id),
        "matched_dealers": len(eligible_dealers),
        "delivered": delivered,
        "failed": failed,
        "status": car_lead.status,
    }
    logger.info(f"lead_matcher complete: {result}")
    return result
