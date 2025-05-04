from pydantic import BaseModel, Field
from typing import Optional, List
import enum

class SlotStatusEnum(str, enum.Enum):
    free = "free"
    occupied = "occupied"
    maintenance = "maintenance"
    
class ParkingSlotBase(BaseModel):
    floor: int = Field(..., ge=0)
    slot_identifier: str = Field(..., min_length=1)
    status: SlotStatusEnum = SlotStatusEnum.free
    label: Optional[str] = Field(None, max_length=100)

class ParkingSlotUpdate(BaseModel):
    floor: Optional[int] = Field(None, ge=0)
    slot_identifier: Optional[str] = Field(None, min_length=1)
    status: Optional[SlotStatusEnum] = None
    label: Optional[str] = Field(None, max_length=100)

class ParkingSlotBulkUpdate(BaseModel):
    slot_ids: List[int] = Field(..., min_items=1)
    status: Optional[SlotStatusEnum] = None
    label: Optional[str] = Field(None, max_length=100)


class ParkingSlotCreate(ParkingSlotBase):
    pass


class ParkingSlot(ParkingSlotBase):
    id: int

    class Config:
        orm_mode = True


class ParkingSlotBulkCreate(BaseModel):
    slots: List[ParkingSlotCreate]
    
class MaintenanceRequest(BaseModel):
    slot_ids: List[int]
    enable: bool = True

