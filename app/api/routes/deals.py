from fastapi import APIRouter
from services.deal_service import get_deals
from services.deal_analyzer import analyze_deal

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.get("/")
def list_deals():
    return get_deals()

@router.post("/analyze")
def analyze(data: dict):
    return analyze_deal(
        data["price"],
        data["arv"],
        data["repair"]
    )
