
from fastapi import APIRouter

router = APIRouter(prefix="/finance",tags=["finance"])

@router.post("/apply")
def apply(application:dict):
    return {"status":"submitted","application":application}
