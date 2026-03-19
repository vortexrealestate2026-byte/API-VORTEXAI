from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_admin_user, get_current_user
from app.database import get_db
from app.models.buyer import Buyer
from app.models.user import User
from app.schemas.buyer import BuyerCreate, BuyerOut, BuyerUpdate

router = APIRouter(prefix="/buyers", tags=["buyers"])


@router.get("", response_model=List[BuyerOut])
def list_buyers(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    return db.query(Buyer).order_by(Buyer.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=BuyerOut, status_code=status.HTTP_201_CREATED)
def create_buyer(
    buyer_in: BuyerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    buyer = Buyer(
        user_id=current_user.id,
        name=buyer_in.name,
        email=buyer_in.email,
        phone=buyer_in.phone,
        zip_codes=buyer_in.zip_codes,
        max_budget=buyer_in.max_budget,
        buyer_type=buyer_in.buyer_type,
        is_active=True,
    )
    db.add(buyer)
    db.commit()
    db.refresh(buyer)
    return buyer


@router.put("/{buyer_id}", response_model=BuyerOut)
def update_buyer(
    buyer_id: UUID,
    buyer_in: BuyerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    if current_user.role != "admin" and buyer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    update_data = buyer_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(buyer, field, value)
    db.commit()
    db.refresh(buyer)
    return buyer


@router.get("/my", response_model=BuyerOut)
def my_buyer_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    buyer = db.query(Buyer).filter(Buyer.user_id == current_user.id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer profile not found")
    return buyer
