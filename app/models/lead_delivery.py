import uuid
from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from app.models.base import Base


class LeadDelivery(Base):
    __tablename__ = "lead_deliveries"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    car_lead_id = Column(UUID(as_uuid=True), ForeignKey("car_leads.id", ondelete="CASCADE"), nullable=False, index=True)
    dealer_id = Column(UUID(as_uuid=True), ForeignKey("dealers.id", ondelete="CASCADE"), nullable=False, index=True)
    delivered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    webhook_response_code = Column(Integer, nullable=True)
    billed = Column(Boolean, default=False, nullable=False)
    stripe_usage_record_id = Column(String, nullable=True)
