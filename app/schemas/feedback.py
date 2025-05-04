from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FeedbackBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    booking_id: Optional[int] = None
    parking_slot_id: Optional[int] = None


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True