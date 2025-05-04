from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

from app.schemas.booking import BookingStatusEnum


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    parking_slot_id = Column(Integer, ForeignKey("parking_slots.id"))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(BookingStatusEnum), default=BookingStatusEnum.active)  # 'active', 'completed', 'cancelled'

    user = relationship("User")
    parking_slot = relationship("ParkingSlot")
