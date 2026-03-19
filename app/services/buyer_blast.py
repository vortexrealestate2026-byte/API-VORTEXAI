import logging

from sqlalchemy.orm import Session

from app.models.buyer import Buyer
from app.models.lead import Lead
from app.services.sendgrid_service import SendGridService
from app.services.twilio_service import TwilioService

logger = logging.getLogger("vortex.buyer_blast")


def blast_buyers_for_signed_contract(lead_id: str, db: Session) -> dict:
    """
    Orchestrates buyer notification after a contract is signed.
    1. Gets the lead from DB
    2. Finds top 10 active buyers in the same zip code
    3. Sends Twilio SMS to each buyer with a phone number
    4. Sends SendGrid email to each buyer
    5. Logs all delivery results
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        logger.error(f"blast_buyers: lead {lead_id} not found")
        return {"error": "Lead not found"}

    buyers = (
        db.query(Buyer)
        .filter(
            Buyer.is_active == True,
            Buyer.zip_codes.any(lead.zip_code),
        )
        .limit(10)
        .all()
    )

    if not buyers:
        logger.info(f"blast_buyers: no active buyers found for zip {lead.zip_code} (lead {lead_id})")
        return {"lead_id": lead_id, "buyers_found": 0, "sms_sent": 0, "emails_sent": 0}

    twilio_svc = TwilioService()
    sendgrid_svc = SendGridService()

    sms_sent = twilio_svc.blast_buyers(lead, buyers, db)
    emails_sent = sendgrid_svc.blast_buyers_email(lead, buyers, db)

    result = {
        "lead_id": lead_id,
        "buyers_found": len(buyers),
        "sms_sent": sms_sent,
        "emails_sent": emails_sent,
    }
    logger.info(f"blast_buyers complete: {result}")
    return result
