from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookingStatusEnum(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"
    
class BookingBase(BaseModel):
    parking_slot_id: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    status: Optional[BookingStatusEnum] = None
    end_time: Optional[datetime] = None


class Booking(BookingBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: BookingStatusEnum

    class Config:
        orm_mode = True
