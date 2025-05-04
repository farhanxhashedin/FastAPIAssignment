from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate


def get_feedback(db: Session, feedback_id: int) -> Optional[Feedback]:
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def get_feedback_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
    return db.query(Feedback).filter(Feedback.user_id == user_id).offset(skip).limit(limit).all()


def get_feedback_by_booking(db: Session, booking_id: int) -> List[Feedback]:
    return db.query(Feedback).filter(Feedback.booking_id == booking_id).all()


def get_feedback_by_parking_slot(db: Session, parking_slot_id: int, skip: int = 0, limit: int = 100) -> List[Feedback]:
    return db.query(Feedback).filter(Feedback.parking_slot_id == parking_slot_id).offset(skip).limit(limit).all()


def get_all_feedback(db: Session, skip: int = 0, limit: int = 100) -> List[Feedback]:
    return db.query(Feedback).offset(skip).limit(limit).all()


def create_feedback(db: Session, feedback: FeedbackCreate, user_id: int) -> Feedback:
    db_feedback = Feedback(
        user_id=user_id,
        booking_id=feedback.booking_id,
        parking_slot_id=feedback.parking_slot_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback