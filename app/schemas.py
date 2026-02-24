from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class TrainStatus(str, Enum):
    ON_TIME = "on_time"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class BookingStatus(str, Enum):
    CONFIRMED = "confirmed"
    PENDING = "pending"
    CANCELLED = "cancelled"


class Train(BaseModel):
    train_id: int
    train_name: str
    from_station: str
    to_station: str
    departure_time: str
    arrival_time: str
    total_seats: int
    available_seats: int
    fare: float
    status: TrainStatus = TrainStatus.ON_TIME


class TrainSearch(BaseModel):
    from_station: str
    to_station: str
    date: str


class Booking(BaseModel):
    booking_id: int
    user_id: int
    train_id: int
    seats: int
    total_amount: float
    status: BookingStatus
    booking_date: str


class BookingRequest(BaseModel):
    train_id: int
    seats: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class User(BaseModel):
    user_id: int
    email: EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PaymentRequest(BaseModel):
    booking_id: int
    payment_method: str = "stripe"

# Add to existing schemas.py
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
