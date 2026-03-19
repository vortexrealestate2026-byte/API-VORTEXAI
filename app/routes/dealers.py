from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_admin_user, get_current_user
from app.core.logging import log_event
from app.database import get_db
from app.models.dealer import Dealer
from app.models.user import User
from app.schemas.dealer import DealerCreate, DealerOut, DealerUpdate
from app.services.stripe_service import StripeService

router = APIRouter(prefix="/dealers", tags=["dealers"])


@router.get("", response_model=List[DealerOut])
def list_dealers(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return db.query(Dealer).order_by(Dealer.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=DealerOut, status_code=status.HTTP_201_CREATED)
def create_dealer(
    dealer_in: DealerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dealer = Dealer(
        user_id=current_user.id,
        company_name=dealer_in.company_name,
        contact_name=dealer_in.contact_name,
        email=dealer_in.email,
        phone=dealer_in.phone,
        province=dealer_in.province,
        credit_tiers=dealer_in.credit_tiers,
        vehicle_types=dealer_in.vehicle_types,
        monthly_lead_cap=dealer_in.monthly_lead_cap,
        per_lead_rate=dealer_in.per_lead_rate,
        crm_webhook_url=dealer_in.crm_webhook_url,
        is_active=True,
    )
    db.add(dealer)
    db.flush()

    stripe_svc = StripeService()
    try:
        customer_id = stripe_svc.create_customer(dealer)
        dealer.stripe_customer_id = customer_id
        subscription_id = stripe_svc.create_metered_subscription(dealer)
        dealer.stripe_subscription_id = subscription_id
        log_event(db, "info", "stripe", f"Stripe setup complete for dealer {dealer.id}")
    except Exception as exc:
        log_event(db, "error", "stripe", f"Stripe setup failed for dealer: {exc}")

    db.commit()
    db.refresh(dealer)
    return dealer


@router.put("/{dealer_id}", response_model=DealerOut)
def update_dealer(
    dealer_id: UUID,
    dealer_in: DealerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dealer = db.query(Dealer).filter(Dealer.id == dealer_id).first()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer not found")
    if current_user.role != "admin" and dealer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    update_data = dealer_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dealer, field, value)
    db.commit()
    db.refresh(dealer)
    return dealer


@router.get("/my", response_model=DealerOut)
def my_dealer_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dealer = db.query(Dealer).filter(Dealer.user_id == current_user.id).first()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    return dealer


@router.get("/my/billing")
def my_billing(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    dealer = db.query(Dealer).filter(Dealer.user_id == current_user.id).first()
    if not dealer:
        raise HTTPException(status_code=404, detail="Dealer profile not found")
    stripe_svc = StripeService()
    return stripe_svc.get_billing_summary(dealer)
