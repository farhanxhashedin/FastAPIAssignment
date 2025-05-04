from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.parking_slot import ParkingSlot
from app.schemas.parking_slot import ParkingSlotCreate, ParkingSlotUpdate, ParkingSlotBulkUpdate


def get_parking_slot(db: Session, slot_id: int) -> Optional[ParkingSlot]:
    return db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()


def get_parking_slot_by_identifier(db: Session, slot_identifier: str) -> Optional[ParkingSlot]:
    return db.query(ParkingSlot).filter(ParkingSlot.slot_identifier == slot_identifier).first()


def get_parking_slots(db: Session, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
    return db.query(ParkingSlot).offset(skip).limit(limit).all()


def get_available_parking_slots(db: Session, skip: int = 0, limit: int = 100) -> List[ParkingSlot]:
    return db.query(ParkingSlot).filter(ParkingSlot.status == "free").offset(skip).limit(limit).all()


def create_parking_slot(db: Session, parking_slot: ParkingSlotCreate) -> ParkingSlot:
    db_slot = ParkingSlot(
        slot_identifier=parking_slot.slot_identifier,
        status=parking_slot.status,
        label=parking_slot.label,
        floor=parking_slot.floor
    )
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def update_parking_slot(db: Session, slot_id: int, parking_slot: ParkingSlotUpdate) -> Optional[ParkingSlot]:
    db_slot = get_parking_slot(db, slot_id)
    if not db_slot:
        return None
    
    update_data = parking_slot.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_slot, key, value)
    
    db.commit()
    db.refresh(db_slot)
    return db_slot


def delete_parking_slot(db: Session, slot_id: int) -> bool:
    db_slot = get_parking_slot(db, slot_id)
    if not db_slot:
        return False
    
    db.delete(db_slot)
    db.commit()
    return True


def bulk_create_parking_slots(db: Session, parking_slots: List[ParkingSlotCreate]) -> List[ParkingSlot]:
    db_slots = []
    for slot in parking_slots:
        db_slot = ParkingSlot(
            slot_identifier=slot.slot_identifier,
            status=slot.status,
            label=slot.label,
            floor=slot.floor
        )
        db.add(db_slot)
        db_slots.append(db_slot)
    
    db.commit()
    for slot in db_slots:
        db.refresh(slot)
    
    return db_slots


def bulk_update_parking_slots(db: Session, update: ParkingSlotBulkUpdate) -> List[ParkingSlot]:
    db_slots = []
    update_data = update.dict(exclude={"slot_ids"}, exclude_unset=True)
    
    for slot_id in update.slot_ids:
        db_slot = get_parking_slot(db, slot_id)
        if db_slot:
            for key, value in update_data.items():
                if value is not None:
                    setattr(db_slot, key, value)
            db_slots.append(db_slot)
    
    db.commit()
    for slot in db_slots:
        db.refresh(slot)
    
    return db_slots