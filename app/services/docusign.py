"""
DocuSign eSignature API for sending contracts to sellers.
"""
import logging
from datetime import datetime

import docusign_esign as docusign
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer
from docusign_esign import SignHere, Tabs, Recipients
from sqlalchemy.orm import Session

from app.config import settings
from app.models.contract import Contract
from app.models.lead import Lead

logger = logging.getLogger("vortex.docusign")


PURCHASE_AGREEMENT_HTML = """
<!DOCTYPE html>
<html>
<head><title>Wholesale Purchase Agreement</title></head>
<body style="font-family: Arial, sans-serif; padding: 40px;">
<h1>Wholesale Real Estate Purchase Agreement</h1>
<p>This Purchase Agreement ("Agreement") is entered into as of the date signed below, between:</p>
<p><strong>Seller:</strong> {owner_name}<br/>
<strong>Property Address:</strong> {address}, {city}, {state} {zip_code}</p>
<p><strong>Buyer:</strong> VortexAI Investments LLC</p>
<h2>Terms and Conditions</h2>
<ol>
  <li><strong>Purchase Price:</strong> The agreed purchase price is ${suggested_offer:,.2f}.</li>
  <li><strong>Closing Date:</strong> Closing shall occur within 21 days of contract execution.</li>
  <li><strong>Property Condition:</strong> Property is sold AS-IS. Buyer accepts property in its current condition.</li>
  <li><strong>Earnest Money:</strong> $1,000 earnest money deposit due within 3 business days.</li>
  <li><strong>Assignment:</strong> Buyer reserves the right to assign this contract to a third party.</li>
  <li><strong>Contingencies:</strong> This agreement is contingent upon satisfactory inspection within 7 days.</li>
  <li><strong>Closing Costs:</strong> Each party to pay their own closing costs unless otherwise agreed.</li>
</ol>
<p>Seller acknowledges they have read and understand all terms of this agreement.</p>
<br/><br/>
<p>Seller Signature: ___________________________  Date: _______________</p>
<p>Seller Name (Print): {owner_name}</p>
</body>
</html>
"""


class DocuSignService:
    def __init__(self):
        self.account_id = settings.DOCUSIGN_ACCOUNT_ID
        self.integration_key = settings.DOCUSIGN_INTEGRATION_KEY
        self.secret_key = settings.DOCUSIGN_SECRET_KEY
        self.base_url = settings.DOCUSIGN_BASE_URL

    def get_access_token(self) -> str:
        api_client = ApiClient()
        api_client.set_base_path(self.base_url)
        try:
            token_response = api_client.request_jwt_application_token(
                client_id=self.integration_key,
                oauth_host_name="account.docusign.com",
                private_key_bytes=self.secret_key.encode("utf-8"),
                expires_in=3600,
                scopes=["signature", "impersonation"],
            )
            return token_response.access_token
        except Exception as exc:
            logger.error(f"DocuSign OAuth error: {exc}")
            raise

    def _get_api_client(self) -> ApiClient:
        access_token = self.get_access_token()
        api_client = ApiClient()
        api_client.set_base_path(self.base_url)
        api_client.set_default_header("Authorization", f"Bearer {access_token}")
        return api_client

    def send_contract(self, lead: Lead, db: Session) -> str:
        suggested_offer = float(lead.suggested_offer) if lead.suggested_offer else 0.0
        html_content = PURCHASE_AGREEMENT_HTML.format(
            owner_name=lead.owner_name or "Property Owner",
            address=lead.address,
            city=lead.city,
            state=lead.state,
            zip_code=lead.zip_code,
            suggested_offer=suggested_offer,
        )

        document = Document(
            document_base64=_b64encode_str(html_content),
            name="Wholesale Purchase Agreement",
            file_extension="html",
            document_id="1",
        )

        signer = Signer(
            email=lead.phone or f"seller+{lead.id}@vortexai.com",
            name=lead.owner_name or "Property Owner",
            recipient_id="1",
            routing_order="1",
        )

        sign_here = SignHere(
            document_id="1",
            page_number="1",
            recipient_id="1",
            tab_label="SignHereTab",
            x_position="200",
            y_position="700",
        )

        signer.tabs = Tabs(sign_here_tabs=[sign_here])

        envelope_definition = EnvelopeDefinition(
            email_subject="Please Sign Your Purchase Agreement - VortexAI",
            documents=[document],
            recipients=Recipients(signers=[signer]),
            status="sent",
        )

        try:
            api_client = self._get_api_client()
            envelopes_api = EnvelopesApi(api_client)
            results = envelopes_api.create_envelope(
                account_id=self.account_id,
                envelope_definition=envelope_definition,
            )
            envelope_id = results.envelope_id
        except Exception as exc:
            logger.error(f"DocuSign send_contract error for lead {lead.id}: {exc}")
            raise

        contract = Contract(
            lead_id=lead.id,
            docusign_envelope_id=envelope_id,
            status="sent",
            sent_at=datetime.utcnow(),
        )
        db.add(contract)

        lead.status = "contract_sent"
        db.commit()
        db.refresh(contract)

        logger.info(f"Contract sent for lead {lead.id}, envelope_id={envelope_id}")
        return envelope_id

    def handle_webhook(self, payload: dict, db: Session) -> None:
        envelope_id = payload.get("envelopeId") or payload.get("data", {}).get("envelopeId")
        new_status_raw = payload.get("status") or payload.get("data", {}).get("envelopeSummary", {}).get("status")
        if not envelope_id:
            logger.warning("DocuSign webhook received without envelopeId")
            return

        status_map = {
            "sent": "sent",
            "delivered": "delivered",
            "completed": "signed",
            "declined": "declined",
            "voided": "voided",
        }
        new_status = status_map.get(str(new_status_raw).lower(), "sent")

        contract = db.query(Contract).filter(Contract.docusign_envelope_id == envelope_id).first()
        if not contract:
            logger.warning(f"Contract not found for envelope_id={envelope_id}")
            return

        contract.status = new_status
        if new_status == "signed":
            contract.signed_at = datetime.utcnow()
            lead = db.query(Lead).filter(Lead.id == contract.lead_id).first()
            if lead:
                lead.status = "signed"

        db.commit()

        if new_status == "signed":
            from app.services.buyer_blast import blast_buyers_for_signed_contract
            try:
                blast_buyers_for_signed_contract(str(contract.lead_id), db)
            except Exception as exc:
                logger.error(f"buyer_blast error after DocuSign signed event: {exc}")


def _b64encode_str(content: str) -> str:
    import base64
    return base64.b64encode(content.encode("utf-8")).decode("utf-8")
