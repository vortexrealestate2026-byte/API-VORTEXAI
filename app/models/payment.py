import uuid
from sqlalchemy import Column, String, Numeric, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from app.models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    dealer_id = Column(UUID(as_uuid=True), ForeignKey("dealers.id", ondelete="SET NULL"), nullable=True, index=True)
    stripe_payment_intent_id = Column(String, nullable=False, unique=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="cad", nullable=False)
    status = Column(
        Enum("pending", "succeeded", "failed", name="payment_status_enum"),
        nullable=False,
        default="pending",
    )
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
