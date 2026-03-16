from fastapi import APIRouter
from app.database import SessionLocal
from app.models.deal import Deal

router = APIRouter()


@router.get("/map/deals")
def get_map_deals():

    db = SessionLocal()

    deals = db.query(Deal).all()

    results = []

    for deal in deals:

        results.append({
            "city": deal.city,
            "price": deal.price,
            "lat": deal.latitude,
            "lng": deal.longitude
        })

    db.close()

    return results
