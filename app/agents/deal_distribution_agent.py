from app.database import SessionLocal
from app.models.deal import Deal
from app.models.buyer import Buyer
from app.notifications.email import send_email


def distribute_deals():

    db = SessionLocal()

    deals = db.query(Deal).filter(Deal.score > 80).all()
    buyers = db.query(Buyer).all()

    for deal in deals:

        for buyer in buyers:

            if buyer.city == deal.city:

                send_email(
                    buyer.email,
                    "New Deal Available",
                    f"Deal in {deal.city} price {deal.price}"
                )
