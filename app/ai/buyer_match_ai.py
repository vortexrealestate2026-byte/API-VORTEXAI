from app.models.deal import Deal
from app.models.buyer import Buyer
from app.database import SessionLocal


def match_buyers():

    db = SessionLocal()

    deals = db.query(Deal).all()
    buyers = db.query(Buyer).all()

    for deal in deals:

        for buyer in buyers:

            if deal.city == buyer.city:

                print(f"Match found: {buyer.email} -> {deal.address}")
