from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_admin_user
from app.schemas.parking_slot import ParkingSlotUpdate
from app.crud import bulk_update_parking_slots
from app.models.user import User
from app.models.parking_slot import SlotStatusEnum
from app.schemas.parking_slot import MaintenanceRequest

router = APIRouter()


@router.post("/maintenance", status_code=status.HTTP_200_OK)
def set_maintenance_mode(
    request: MaintenanceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    status_value = SlotStatusEnum.maintenance if request.enable else SlotStatusEnum.free
    update = ParkingSlotUpdate(status=status_value)

    updated_slots = []
    for slot_id in request.slot_ids:
        from app.crud.parking_slot import update_parking_slot
        slot = update_parking_slot(db, slot_id, update)
        if slot:
            updated_slots.append(slot)

    if not updated_slots:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No valid parking slots found",
        )

    return {"message": f"Updated {len(updated_slots)} slots to {status_value} status"}