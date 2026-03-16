from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
import datetime

router = APIRouter()

SECRET = "SUPER_SECRET_KEY"


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest):

    # Example user validation
    if data.email != "admin@vortex.ai" or data.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "email": data.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    return {"access_token": token}
