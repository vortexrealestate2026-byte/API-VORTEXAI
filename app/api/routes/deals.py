from fastapi import APIRouter
from services.deal_service import get_deals

router = APIRouter(prefix="/deals", tags=["Deals"])

@router.get("/")
def deals():
    return get_deals()
