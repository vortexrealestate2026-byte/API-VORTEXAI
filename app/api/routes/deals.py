from fastapi import APIRouter
from app.services.deal_service import get_deals

router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)

@router.get("/")
def get_all_deals():
    """
    Endpoint to retrieve available deals.
    """
    return get_deals()
