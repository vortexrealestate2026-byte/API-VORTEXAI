from app.database import SessionLocal
from app.models.deal import Deal
from collections import defaultdict


def analyze_city_demand():

    db = SessionLocal()

    deals = db.query(Deal).all()

    city_counts = defaultdict(int)

    for deal in deals:
        city_counts[deal.city] += 1

    demand_map = sorted(
        city_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    db.close()

    return demand_map
