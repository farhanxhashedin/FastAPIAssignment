from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_active_user, get_admin_user
from app.schemas.booking import Booking, BookingCreate, BookingUpdate
from app.crud import (
    get_booking, get_bookings_by_user, get_all_bookings, create_booking, 
    update_booking, cancel_booking
)
from app.models.user import User
from app.schemas.user import UserRoleEnum


router = APIRouter()


@router.get("/", response_model=List[Booking])
def read_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if current_user.role == UserRoleEnum.admin:
        return get_all_bookings(db, skip=skip, limit=limit)
    return get_bookings_by_user(db, user_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking_endpoint(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # Only regular users can make bookings, not admins
    if current_user.role == UserRoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot make bookings",
        )
    
    db_booking = create_booking(db=db, booking=booking, user_id=current_user.id)
    if db_booking is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The parking slot is not available",
        )
    return db_booking


@router.get("/{booking_id}", response_model=Booking)
def read_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_booking = get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Regular users can only view their own bookings
    if current_user.role != UserRoleEnum.admin and db_booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return db_booking


@router.put("/{booking_id}", response_model=Booking)
def update_booking_endpoint(
    booking_id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # Check if the booking exists
    db_booking = get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Admins can update any booking, regular users only their own
    if current_user.role == UserRoleEnum.admin:
        db_booking = update_booking(db, booking_id, booking, db_booking.user_id)
    else:
        db_booking = update_booking(db, booking_id, booking, current_user.id)
        if db_booking is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
    
    return db_booking


@router.post("/{booking_id}/cancel", response_model=Booking)
def cancel_booking_endpoint(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    # Check if the booking exists
    db_booking = get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Admins can cancel any booking, regular users only their own
    if current_user.role == UserRoleEnum.admin:
        db_booking = cancel_booking(db, booking_id, db_booking.user_id)
    else:
        db_booking = cancel_booking(db, booking_id, current_user.id)
        if db_booking is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
    
    return db_booking