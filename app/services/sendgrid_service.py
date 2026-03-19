import logging
from typing import List

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy.orm import Session

from app.config import settings
from app.models.buyer import Buyer
from app.models.lead import Lead

logger = logging.getLogger("vortex.sendgrid")


class SendGridService:
    def __init__(self):
        self.client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        self.from_email = settings.SENDGRID_FROM_EMAIL

    def send_email(self, to_email: str, subject: str, html_content: str) -> bool:
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=html_content,
        )
        try:
            response = self.client.send(message)
            logger.info(f"Email sent to {to_email}: status={response.status_code}")
            return response.status_code in (200, 201, 202)
        except Exception as exc:
            logger.error(f"SendGrid error to {to_email}: {exc}")
            return False

    def blast_buyers_email(self, lead: Lead, buyers: List[Buyer], db: Session) -> int:
        arv = f"${float(lead.arv):,.0f}" if lead.arv else "TBD"
        offer = f"${float(lead.suggested_offer):,.0f}" if lead.suggested_offer else "TBD"
        equity = f"${float(lead.estimated_equity):,.0f}" if lead.estimated_equity else "TBD"
        distress = lead.distress_type.replace("_", " ").title()

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
          <div style="background: #1a1a2e; color: white; padding: 20px; border-radius: 8px 8px 0 0;">
            <h1 style="margin:0;">🏠 Deal Alert - VortexAI</h1>
          </div>
          <div style="background: #f9f9f9; padding: 20px; border-radius: 0 0 8px 8px;">
            <h2>{lead.address}</h2>
            <p>{lead.city}, {lead.state} {lead.zip_code}</p>
            <table style="width:100%; border-collapse: collapse;">
              <tr style="background:#e8f4fd;">
                <td style="padding:10px; font-weight:bold;">Distress Type</td>
                <td style="padding:10px;">{distress}</td>
              </tr>
              <tr>
                <td style="padding:10px; font-weight:bold;">Estimated Equity</td>
                <td style="padding:10px;">{equity}</td>
              </tr>
              <tr style="background:#e8f4fd;">
                <td style="padding:10px; font-weight:bold;">After Repair Value (ARV)</td>
                <td style="padding:10px; color:#27ae60; font-size:1.2em;">{arv}</td>
              </tr>
              <tr>
                <td style="padding:10px; font-weight:bold;">Suggested Offer</td>
                <td style="padding:10px; color:#e74c3c; font-size:1.2em;">{offer}</td>
              </tr>
            </table>
            <br/>
            <p style="background:#27ae60; color:white; padding:12px; border-radius:6px; text-align:center;">
              <strong>Reply to this email or call us to express interest in this deal!</strong>
            </p>
            <p style="color:#999; font-size:0.8em;">You are receiving this because you are a registered buyer with VortexAI.
            To unsubscribe, reply with STOP.</p>
          </div>
        </body>
        </html>
        """

        subject = f"🏠 New Deal: {lead.address}, {lead.city}, {lead.state} - ARV {arv}"
        sent_count = 0
        for buyer in buyers:
            success = self.send_email(buyer.email, subject, html_content)
            if success:
                sent_count += 1

        logger.info(f"Buyer email blast for lead {lead.id}: {sent_count}/{len(buyers)} sent")
        return sent_count
