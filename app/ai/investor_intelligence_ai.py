from app.database import SessionLocal
from app.models.buyer import Buyer
from app.models.deal import Deal


def rank_investors():

    db = SessionLocal()

    buyers = db.query(Buyer).all()

    rankings = []

    for buyer in buyers:

        deals = db.query(Deal).filter(
            Deal.buyer_id == buyer.id
        ).count()

        rankings.append({
            "buyer": buyer.email,
            "city": buyer.city,
            "deals_closed": deals
        })

    db.close()

    rankings.sort(key=lambda x: x["deals_closed"], reverse=True)

    return rankings
