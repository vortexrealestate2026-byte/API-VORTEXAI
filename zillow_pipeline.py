
from fastapi import APIRouter

router = APIRouter(prefix="/buyers",tags=["buyers"])

@router.post("/")
def add_buyer(buyer:dict):
    return {"status":"stored","buyer":buyer}
