import hashlib
import hmac
import json
import logging

import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.logging import log_event
from app.database import get_db
from app.models.payment import Payment
from app.services.docusign import DocuSignService

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
logger = logging.getLogger("vortex.webhooks")


@router.post("/docusign")
async def docusign_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """DocuSign Connect webhook handler. Verifies HMAC and processes envelope status updates."""
    body_bytes = await request.body()

    signature = request.headers.get("X-DocuSign-Signature-1", "")
    if signature:
        expected = hmac.new(
            settings.DOCUSIGN_SECRET_KEY.encode("utf-8"),
            body_bytes,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, signature):
            log_event(db, "warning", "docusign", "Webhook HMAC verification failed")
            raise HTTPException(status_code=401, detail="Invalid DocuSign signature")

    try:
        payload = json.loads(body_bytes)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    log_event(db, "info", "docusign", "DocuSign webhook received", details={"envelope_id": payload.get("envelopeId")})

    docusign_svc = DocuSignService()
    try:
        docusign_svc.handle_webhook(payload, db)
    except Exception as exc:
        log_event(db, "error", "docusign", f"Webhook processing error: {exc}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

    return {"status": "ok"}


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """Stripe webhook handler. Verifies signature and processes payment events."""
    body_bytes = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            body_bytes,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError:
        log_event(db, "warning", "stripe", "Stripe webhook signature verification failed")
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Webhook error: {exc}")

    event_type = event.get("type")
    log_event(db, "info", "stripe", f"Stripe event received: {event_type}", details={"event_id": event.get("id")})

    if event_type == "payment_intent.succeeded":
        pi = event["data"]["object"]
        payment = Payment(
            stripe_payment_intent_id=pi["id"],
            amount=pi["amount"] / 100,
            currency=pi.get("currency", "cad"),
            status="succeeded",
            description=pi.get("description", ""),
        )
        db.add(payment)
        db.commit()

    elif event_type == "payment_intent.payment_failed":
        pi = event["data"]["object"]
        payment = Payment(
            stripe_payment_intent_id=pi["id"],
            amount=pi["amount"] / 100,
            currency=pi.get("currency", "cad"),
            status="failed",
            description=pi.get("description", ""),
        )
        db.add(payment)
        db.commit()

    return {"status": "ok"}
