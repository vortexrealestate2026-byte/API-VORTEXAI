from fastapi import APIRouter
from app.ai.deal_scoring_ai import score_deal

router = APIRouter(prefix="/ai")

@router.post("/score-deal")
def score(data: dict):
    return score_deal(data)
