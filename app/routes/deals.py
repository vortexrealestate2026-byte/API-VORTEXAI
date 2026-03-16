from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.deal import Deal

router = APIRouter(prefix="/deals", tags=["Deals"])


@router.get("/")
def get_deals(db: Session = Depends(get_db)):

    deals = db.query(Deal).all()

    return deals


@router.get("/{deal_id}")
def get_deal(deal_id: int, db: Session = Depends(get_db)):

    deal = db.query(Deal).filter(Deal.id == deal_id).first()

    return deal


@router.post("/")
def create_deal(data: dict, db: Session = Depends(get_db)):

    deal = Deal(
        title=data["title"],
        city=data["city"],
        price=data["price"],
        arv=data["arv"]
    )

    db.add(deal)
    db.commit()
    db.refresh(deal)

    return deal
