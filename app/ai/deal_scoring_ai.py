from app.database import SessionLocal
from app.models.deal import Deal

def score_deals():

    db = SessionLocal()

    deals = db.query(Deal).all()

    for deal in deals:

        score = 0

        if deal.profit_margin > 20000:
            score += 40

        if deal.repair_cost < 50000:
            score += 20

        if deal.city in ["Dallas", "Phoenix", "Atlanta"]:
            score += 30

        deal.score = score

    db.commit()
