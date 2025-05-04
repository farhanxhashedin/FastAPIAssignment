from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.token import Token, TokenData
from app.schemas.parking_slot import (
    ParkingSlot, ParkingSlotCreate, ParkingSlotUpdate, ParkingSlotBulkCreate, ParkingSlotBulkUpdate
)
from app.schemas.booking import Booking, BookingCreate, BookingUpdate
from app.schemas.feedback import Feedback, FeedbackCreate