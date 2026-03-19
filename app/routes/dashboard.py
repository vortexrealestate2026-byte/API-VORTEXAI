from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.auth import get_admin_user
from app.database import get_db
from app.models.car_lead import CarLead
from app.models.contract import Contract
from app.models.dealer import Dealer
from app.models.lead import Lead
from app.models.lead_delivery import LeadDelivery
from app.models.payment import Payment
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    """Admin dashboard: aggregated stats across both business lines."""
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_re_leads = db.query(func.count(Lead.id)).scalar() or 0
    leads_by_status_rows = (
        db.query(Lead.status, func.count(Lead.id))
        .group_by(Lead.status)
        .all()
    )
    leads_by_status = {row[0]: row[1] for row in leads_by_status_rows}

    total_car_leads = db.query(func.count(CarLead.id)).scalar() or 0
    car_leads_by_province_rows = (
        db.query(CarLead.province, func.count(CarLead.id))
        .group_by(CarLead.province)
        .all()
    )
    car_leads_by_province = {row[0]: row[1] for row in car_leads_by_province_rows}

    active_contracts = (
        db.query(func.count(Contract.id))
        .filter(Contract.status.in_(["sent", "delivered"]))
        .scalar() or 0
    )
    signed_this_month = (
        db.query(func.count(Contract.id))
        .filter(Contract.status == "signed", Contract.signed_at >= month_start)
        .scalar() or 0
    )

    revenue_this_month_row = (
        db.query(func.sum(Payment.amount))
        .filter(Payment.status == "succeeded", Payment.created_at >= month_start)
        .scalar()
    )
    total_revenue_this_month = float(revenue_this_month_row) if revenue_this_month_row else 0.0

    dealer_count = db.query(func.count(Dealer.id)).scalar() or 0
    active_dealer_count = (
        db.query(func.count(Dealer.id)).filter(Dealer.is_active == True).scalar() or 0
    )

    recent_deliveries = (
        db.query(LeadDelivery)
        .order_by(LeadDelivery.delivered_at.desc())
        .limit(10)
        .all()
    )
    recent_lead_deliveries = [
        {
            "id": str(d.id),
            "car_lead_id": str(d.car_lead_id),
            "dealer_id": str(d.dealer_id),
            "delivered_at": d.delivered_at.isoformat() if d.delivered_at else None,
            "billed": d.billed,
            "webhook_response_code": d.webhook_response_code,
        }
        for d in recent_deliveries
    ]

    return {
        "total_real_estate_leads": total_re_leads,
        "leads_by_status": leads_by_status,
        "total_car_leads": total_car_leads,
        "car_leads_by_province": car_leads_by_province,
        "active_contracts": active_contracts,
        "signed_contracts_this_month": signed_this_month,
        "total_revenue_this_month_cad": total_revenue_this_month,
        "dealer_count": dealer_count,
        "active_dealer_count": active_dealer_count,
        "recent_lead_deliveries": recent_lead_deliveries,
        "generated_at": now.isoformat(),
    }
