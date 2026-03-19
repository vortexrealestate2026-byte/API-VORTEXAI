import logging
from typing import List

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from sqlalchemy.orm import Session

from app.config import settings
from app.models.buyer import Buyer
from app.models.lead import Lead

logger = logging.getLogger("vortex.twilio")


class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_phone = settings.TWILIO_PHONE_NUMBER

    def send_sms(self, to_phone: str, message: str) -> bool:
        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.from_phone,
                to=to_phone,
            )
            logger.info(f"SMS sent to {to_phone}: sid={msg.sid}")
            return True
        except TwilioRestException as exc:
            logger.error(f"Twilio SMS error to {to_phone}: {exc}")
            return False

    def blast_buyers(self, lead: Lead, buyers: List[Buyer], db: Session) -> int:
        arv = f"${float(lead.arv):,.0f}" if lead.arv else "TBD"
        offer = f"${float(lead.suggested_offer):,.0f}" if lead.suggested_offer else "TBD"
        message = (
            f"DEAL ALERT - VortexAI\n"
            f"Property: {lead.address}, {lead.city}, {lead.state} {lead.zip_code}\n"
            f"ARV: {arv} | Suggested Offer: {offer}\n"
            f"Type: {lead.distress_type.replace('_', ' ').title()}\n"
            f"Contact us to express interest!"
        )

        sent_count = 0
        for buyer in buyers:
            if buyer.phone:
                success = self.send_sms(buyer.phone, message)
                if success:
                    sent_count += 1

        logger.info(f"Buyer SMS blast for lead {lead.id}: {sent_count}/{len(buyers)} sent")
        return sent_count
