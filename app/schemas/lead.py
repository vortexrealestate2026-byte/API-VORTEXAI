from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class CompProperty(BaseModel):
    address: str
    sale_price: Optional[Decimal] = None
    sqft: Optional[int] = None
    distance_miles: Optional[float] = None
    sale_date: Optional[str] = None


class DealAnalysis(BaseModel):
    arv: Optional[Decimal] = None
    comps: List[CompProperty] = []
    suggested_offer: Optional[Decimal] = None
    estimated_repairs: Decimal = Decimal("30000")
    notes: Optional[str] = None


class LeadCreate(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    estimated_equity: Optional[Decimal] = None
    distress_type: str
    batchdata_id: Optional[str] = None


class LeadUpdate(BaseModel):
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    estimated_equity: Optional[Decimal] = None
    arv: Optional[Decimal] = None
    suggested_offer: Optional[Decimal] = None
    status: Optional[str] = None


class LeadOut(BaseModel):
    id: UUID
    address: str
    city: str
    state: str
    zip_code: str
    owner_name: Optional[str] = None
    phone: Optional[str] = None
    estimated_equity: Optional[Decimal] = None
    distress_type: str
    arv: Optional[Decimal] = None
    suggested_offer: Optional[Decimal] = None
    status: str
    batchdata_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
