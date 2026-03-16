from app.database import SessionLocal
from app.models.deal import Deal


def remove_duplicate_deals():

    db = SessionLocal()

    deals = db.query(Deal).all()

    seen = set()

    for deal in deals:

        key = (deal.address, deal.price)

        if key in seen:

            db.delete(deal)

        else:

            seen.add(key)

    db.commit()

    db.close()
