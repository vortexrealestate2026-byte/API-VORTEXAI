from fastapi import APIRouter
from services.property_scraper import get_properties

router = APIRouter(prefix="/properties", tags=["Properties"])

@router.get("/")
def properties():
    return get_properties()
