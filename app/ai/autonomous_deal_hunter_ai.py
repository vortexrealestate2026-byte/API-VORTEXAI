from app.database import SessionLocal
from app.models.deal import Deal


def hunt_deals():

    db = SessionLocal()

    deals = db.query(Deal).all()

    hot_deals = []

    for deal in deals:

        profit = deal.arv - (deal.price + deal.repair_cost)

        if profit > 30000:
            hot_deals.append(deal)

    db.close()

    return hot_deals
