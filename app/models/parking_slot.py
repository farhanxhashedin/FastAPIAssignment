
from sqlalchemy import Column, String, Integer, Boolean, Enum
from app.database import Base
from app.schemas.parking_slot import SlotStatusEnum



class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    floor = Column(Integer, nullable=False)
    slot_identifier = Column(String, unique=True, index=True)
    status = Column(Enum(SlotStatusEnum), default=SlotStatusEnum.free)
    label = Column(String, nullable=True)