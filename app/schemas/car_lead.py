from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CarLeadCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    province: str
    income_range: str
    credit_score_range: str
    vehicle_type: str


class CarLeadOut(BaseModel):
    id: UUID
    name: str
    phone: str
    email: Optional[str] = None
    province: str
    income_range: str
    credit_score_range: str
    vehicle_type: str
    status: str
    make_webhook_sent: bool
    created_at: datetime

    model_config = {"from_attributes": True}
