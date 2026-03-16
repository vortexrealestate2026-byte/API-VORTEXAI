from fastapi import APIRouter

router = APIRouter()

@router.get("/deals")

def deals():

    return {"deals": []}
