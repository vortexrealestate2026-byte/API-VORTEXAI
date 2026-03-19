from datetime import datetime
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel, EmailStr


class DealerCriteria(BaseModel):
    province: str
    credit_tiers: List[str] = []
    vehicle_types: List[str] = []
    monthly_lead_cap: int = 50


class DealerCreate(BaseModel):
    company_name: str
    contact_name: str
    email: EmailStr
    phone: Optional[str] = None
    province: str
    credit_tiers: Optional[List[str]] = []
    vehicle_types: Optional[List[str]] = []
    monthly_lead_cap: int = 50
    per_lead_rate: Decimal = Decimal("25.00")
    crm_webhook_url: Optional[str] = None


class DealerUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    credit_tiers: Optional[List[str]] = None
    vehicle_types: Optional[List[str]] = None
    monthly_lead_cap: Optional[int] = None
    per_lead_rate: Optional[Decimal] = None
    crm_webhook_url: Optional[str] = None
    is_active: Optional[bool] = None


class DealerOut(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    company_name: str
    contact_name: str
    email: str
    phone: Optional[str] = None
    province: str
    credit_tiers: Optional[List[str]] = []
    vehicle_types: Optional[List[str]] = []
    monthly_lead_cap: int
    leads_this_month: int
    per_lead_rate: Decimal
    crm_webhook_url: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
