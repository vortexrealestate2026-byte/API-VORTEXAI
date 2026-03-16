
from fastapi import APIRouter

router = APIRouter(prefix="/deals",tags=["deals"])

@router.get("/")
def list_deals():
    return {"deals":[]}

@router.post("/")
def create_deal(deal:dict):
    return {"status":"stored","deal":deal}

@router.post("/match/{deal_id}")
def match_buyers(deal_id:int):
    return {"deal_id":deal_id,"buyers":[]}
