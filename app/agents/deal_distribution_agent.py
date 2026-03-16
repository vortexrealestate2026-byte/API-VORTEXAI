from app.database import SessionLocal
from app.models.deal import Deal
from app.models.buyer import Buyer
from app.notifications.email import send_email
import logging

logging.basicConfig(level=logging.INFO)


def distribute_deals():

    db = SessionLocal()

    try:

        deals = db.query(Deal).filter(Deal.score >= 70).all()
        buyers = db.query(Buyer).all()

        logging.info(f"Found {len(deals)} deals")

        for deal in deals:

            for buyer in buyers:

                if buyer.city.lower() == deal.city.lower():

                    subject = f"New Deal in {deal.city}"

                    message = f"""
New Deal Available

City: {deal.city}
Price: ${deal.price}
ARV: ${deal.arv}
Profit Margin: ${deal.profit_margin}

"""

                    send_email(buyer.email, subject, message)

                    logging.info(f"Sent deal {deal.id} to {buyer.email}")

    except Exception as e:

        logging.error(f"Deal distribution error: {e}")

    finally:

        db.close()
