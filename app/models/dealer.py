import uuid
from sqlalchemy import Column, String, Integer, Numeric, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func, text
from app.models.base import Base


class Dealer(Base):
    __tablename__ = "dealers"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    company_name = Column(String, nullable=False)
    contact_name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    province = Column(
        Enum("MB", "SK", "AB", name="province_enum"),
        nullable=False,
    )
    credit_tiers = Column(ARRAY(String), nullable=True, default=list)
    vehicle_types = Column(ARRAY(String), nullable=True, default=list)
    monthly_lead_cap = Column(Integer, default=50, nullable=False)
    leads_this_month = Column(Integer, default=0, nullable=False)
    per_lead_rate = Column(Numeric(8, 2), nullable=False, default=25.00)
    crm_webhook_url = Column(String, nullable=True)
    stripe_customer_id = Column(String, nullable=True)
    stripe_subscription_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
