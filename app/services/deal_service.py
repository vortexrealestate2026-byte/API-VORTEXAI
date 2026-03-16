from app.database import SessionLocal
from app.models.deal import Deal


def create_deal(data):

    db = SessionLocal()

    deal = Deal(**data)

    db.add(deal)
    db.commit()
    db.refresh(deal)

    db.close()

    return deal


def get_all_deals():

    db = SessionLocal()

    deals = db.query(Deal).all()

    db.close()

    return deals
