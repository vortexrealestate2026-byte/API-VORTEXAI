import uuid
from sqlalchemy import Column, String, Numeric, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.sql import func, text
from app.models.base import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"), default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True)
    zip_codes = Column(ARRAY(String), nullable=True, default=list)
    max_budget = Column(Numeric(12, 2), nullable=True)
    buyer_type = Column(
        Enum("flipper", "landlord", "wholesaler", name="buyer_type_enum"),
        nullable=False,
        default="flipper",
    )
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
