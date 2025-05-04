from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_active_user, get_admin_user
from app.schemas.feedback import Feedback, FeedbackCreate
from app.crud import (
    get_feedback, get_feedback_by_user, get_feedback_by_booking, 
    get_feedback_by_parking_slot, get_all_feedback, create_feedback
)
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Feedback])
def read_feedback(
    skip: int = 0,
    limit: int = 100,
    booking_id: int = None,
    parking_slot_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if current_user.role == "admin":
        if booking_id:
            return get_feedback_by_booking(db, booking_id=booking_id)
        elif parking_slot_id:
            return get_feedback_by_parking_slot(db, parking_slot_id=parking_slot_id, skip=skip, limit=limit)
        else:
            return get_all_feedback(db, skip=skip, limit=limit)
    else:
        return get_feedback_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=Feedback, status_code=status.HTTP_201_CREATED)
def create_feedback_endpoint(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_feedback(db=db, feedback=feedback, user_id=current_user.id)


@router.get("/{feedback_id}", response_model=Feedback)
def read_feedback_by_id(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_feedback = get_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # Regular users can only view their own feedback
    if current_user.role != "admin" and db_feedback.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return db_feedback