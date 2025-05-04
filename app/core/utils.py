from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.parking_slot import ParkingSlot
from app.schemas.parking_slot import SlotStatusEnum
from app.schemas.booking import BookingStatusEnum


def check_slot_availability(db: Session, slot_id: int) -> bool:
    """Check if a parking slot is available for booking."""
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()
    if not slot or slot.status != SlotStatusEnum.free:
        return False
    return True


def get_active_bookings_for_user(db: Session, user_id: int) -> List[Booking]:
    """Get all active bookings for a user."""
    return db.query(Booking).filter(Booking.user_id == user_id, Booking.status == BookingStatusEnum.active).all()