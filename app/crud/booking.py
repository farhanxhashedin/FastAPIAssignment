from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.booking import Booking
from app.models.parking_slot import ParkingSlot
from app.schemas.booking import BookingCreate, BookingUpdate
from app.core.utils import check_slot_availability
from app.schemas.parking_slot import SlotStatusEnum
from app.schemas.booking import BookingStatusEnum

def get_booking(db: Session, booking_id: int) -> Optional[Booking]:
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).filter(Booking.user_id == user_id).offset(skip).limit(limit).all()


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[Booking]:
    return db.query(Booking).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BookingCreate, user_id: int) -> Optional[Booking]:
    # Check if the slot is available
    if not check_slot_availability(db, booking.parking_slot_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The parking slot is not available"
        )
    
    # Update the slot status to 'occupied'
    slot = db.query(ParkingSlot).filter(ParkingSlot.id == booking.parking_slot_id).first()
    slot.status = SlotStatusEnum.occupied
    
    # Create the booking
    db_booking = Booking(
        user_id=user_id,
        parking_slot_id=booking.parking_slot_id,
        start_time=datetime.utcnow(),
        status=BookingStatusEnum.active
    )
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking_id: int, booking: BookingUpdate, user_id: int) -> Optional[Booking]:
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    if db_booking.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions to update this booking")
    
    update_data = booking.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_booking, key, value)
    
    # If status changed to 'cancelled' or 'completed', free up the slot
    if db_booking.status in [BookingStatusEnum.cancelled, BookingStatusEnum.completed]:
        slot = db.query(ParkingSlot).filter(ParkingSlot.id == db_booking.parking_slot_id).first()
        if slot:
            slot.status = SlotStatusEnum.free
            
    db.commit()
    db.refresh(db_booking)
    return db_booking


def cancel_booking(db: Session, booking_id: int, user_id: int) -> Optional[Booking]:
    booking_update = BookingUpdate(status=BookingStatusEnum.cancelled, end_time=datetime.utcnow())
    return update_booking(db, booking_id, booking_update, user_id)

