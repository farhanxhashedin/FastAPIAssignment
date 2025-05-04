from fastapi import APIRouter
from app.api.endpoints import auth, users, parking_slots, bookings, feedback, admin

api_router = APIRouter()

# Include all the API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(parking_slots.router, prefix="/parking-slots", tags=["Parking Slots"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])