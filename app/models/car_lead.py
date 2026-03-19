import uuid
from sqlalchemy import Column, String, Boolean, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, text
from app.models.base import Base


class CarLead(Base):
    __tablename__ = "car_leads"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    province = Column(
        Enum("MB", "SK", "AB", name="car_lead_province_enum"),
        nullable=False,
    )
    income_range = Column(
        Enum("under_40k", "40k_60k", "60k_80k", "80k_100k", "over_100k", name="income_range_enum"),
        nullable=False,
    )
    credit_score_range = Column(
        Enum("under_550", "550_599", "600_649", "650_699", "700_749", "750_plus", name="credit_score_range_enum"),
        nullable=False,
    )
    vehicle_type = Column(
        Enum("sedan", "suv", "truck", "van", "electric", name="vehicle_type_enum"),
        nullable=False,
    )
    status = Column(
        Enum("new", "matched", "delivered", "unmatched", name="car_lead_status_enum"),
        nullable=False,
        default="new",
    )
    make_webhook_sent = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
