from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app import schemas, crud
from app.auth import get_current_user 


router = APIRouter()

# Global booking counter (production = DB)
BOOKINGS_DB = []
# Update book_seats endpoint
@router.post("/", response_model=schemas.Booking)
async def book_seats(
    booking_request: schemas.BookingRequest,
    current_user: dict = Depends(get_current_user)  # ✅ Protected!
):
    """Book train seats online (Protected)"""
    # Use real user_id from JWT
    available_seats = crud.check_seats(booking_request.train_id, None)
    trains = crud.load_sample_trains()
    train = next((t for t in trains if t.train_id == booking_request.train_id), None)
    
    if not train or available_seats < booking_request.seats:
        raise HTTPException(status_code=400, detail="No seats available!")
    
    booking = schemas.Booking(
        booking_id=len(BOOKINGS_DB) + 1,
        user_id=current_user["user_id"],  # ✅ Real user ID!
        train_id=booking_request.train_id,
        seats=booking_request.seats,
        total_amount=train.fare * booking_request.seats,
        status=schemas.BookingStatus.CONFIRMED,
        booking_date="2026-02-24T18:00:00"
    )
    
    train.available_seats -= booking_request.seats
    BOOKINGS_DB.append(booking)
    return booking


@router.get("/history/", response_model=List[schemas.Booking])
def get_booking_history():
    """Ticket booking history"""
    if not BOOKINGS_DB:
        return []
    return BOOKINGS_DB[-5:]  # Last 5 bookings

@router.get("/my-bookings/", response_model=List[schemas.Booking])
def my_bookings(user_id: int = 1):  # Simulated auth
    """User's booking history"""
    user_bookings = [b for b in BOOKINGS_DB if b.user_id == user_id]
    return user_bookings
