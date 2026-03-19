from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.core.auth import get_admin_user
from app.database import get_db
from app.models.car_lead import CarLead
from app.models.user import User
from app.schemas.car_lead import CarLeadCreate, CarLeadOut
from app.services.make_webhook import MakeWebhookService
from app.services.lead_matcher import match_and_deliver_lead

router = APIRouter(prefix="/car-leads", tags=["car-leads"])


@router.post("", response_model=CarLeadOut, status_code=status.HTTP_201_CREATED)
def create_car_lead(
    lead_in: CarLeadCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Public endpoint. Creates a car lead, fires Make.com webhook, then triggers async dealer matching."""
    car_lead = CarLead(
        name=lead_in.name,
        phone=lead_in.phone,
        email=lead_in.email,
        province=lead_in.province,
        income_range=lead_in.income_range,
        credit_score_range=lead_in.credit_score_range,
        vehicle_type=lead_in.vehicle_type,
        status="new",
        make_webhook_sent=False,
    )
    db.add(car_lead)
    db.commit()
    db.refresh(car_lead)

    make_svc = MakeWebhookService()
    webhook_sent = make_svc.trigger_car_lead(car_lead)
    if webhook_sent:
        car_lead.make_webhook_sent = True
        db.commit()

    background_tasks.add_task(_async_match, str(car_lead.id))

    return car_lead


def _async_match(car_lead_id: str):
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        match_and_deliver_lead(car_lead_id, db)
    finally:
        db.close()


@router.get("", response_model=List[CarLeadOut])
def list_car_leads(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return db.query(CarLead).order_by(CarLead.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{lead_id}", response_model=CarLeadOut)
def get_car_lead(
    lead_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    from fastapi import HTTPException
    lead = db.query(CarLead).filter(CarLead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Car lead not found")
    return lead
