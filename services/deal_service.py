from app.database import SessionLocal
from app.models.deal import Deal


def create_deal(data):

    db = SessionLocal()

    deal = Deal(**data)

    db.add(deal)
    db.commit()

    return deal
