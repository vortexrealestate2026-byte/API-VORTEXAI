from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, EmailStr


class BuyerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    zip_codes: Optional[List[str]] = []
    max_budget: Optional[Decimal] = None
    buyer_type: str = "flipper"


class BuyerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    zip_codes: Optional[List[str]] = None
    max_budget: Optional[Decimal] = None
    buyer_type: Optional[str] = None
    is_active: Optional[bool] = None


class BuyerOut(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    name: str
    email: str
    phone: Optional[str] = None
    zip_codes: Optional[List[str]] = []
    max_budget: Optional[Decimal] = None
    buyer_type: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
