from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/finance", tags=["Finance"])


class FinanceApplication(BaseModel):

    name: str
    email: str
    phone: str
    income: float
    credit_score: int
    vehicle: str


@router.post("/apply")
def apply_financing(app: FinanceApplication):

    # In production this would submit to lenders
    return {
        "status": "received",
        "applicant": app.name,
        "vehicle": app.vehicle
    }
