from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_active_user, get_admin_user
from app.schemas.parking_slot import (
    ParkingSlot, ParkingSlotCreate, ParkingSlotUpdate, ParkingSlotBulkCreate, ParkingSlotBulkUpdate
)
from app.crud import (
    get_parking_slot, get_parking_slots, get_available_parking_slots, 
    create_parking_slot, update_parking_slot, delete_parking_slot,
    bulk_create_parking_slots, bulk_update_parking_slots
)
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ParkingSlot])
def read_parking_slots(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if status == "free":
        return get_available_parking_slots(db, skip=skip, limit=limit)
    return get_parking_slots(db, skip=skip, limit=limit)


@router.post("/", response_model=ParkingSlot, status_code=status.HTTP_201_CREATED)
def create_parking_slot_endpoint(
    parking_slot: ParkingSlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return create_parking_slot(db=db, parking_slot=parking_slot)


@router.get("/{slot_id}", response_model=ParkingSlot)
def read_parking_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_slot = get_parking_slot(db, slot_id=slot_id)
    if db_slot is None:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return db_slot


@router.put("/{slot_id}", response_model=ParkingSlot)
def update_parking_slot_endpoint(
    slot_id: int,
    parking_slot: ParkingSlotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    db_slot = update_parking_slot(db, slot_id, parking_slot)
    if db_slot is None:
        raise HTTPException(status_code=404, detail="Parking slot not found")
    return db_slot


@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_parking_slot_endpoint(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    result = delete_parking_slot(db, slot_id)
    if not result:
        raise HTTPException(status_code=404, detail="Parking slot not found")


@router.post("/bulk", response_model=List[ParkingSlot], status_code=status.HTTP_201_CREATED)
def create_parking_slots_bulk(
    parking_slots: ParkingSlotBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return bulk_create_parking_slots(db=db, parking_slots=parking_slots.slots)


@router.put("/bulk", response_model=List[ParkingSlot])
def update_parking_slots_bulk(
    update: ParkingSlotBulkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return bulk_update_parking_slots(db=db, update=update)