from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import trains, bookings, users, payments

app = FastAPI(title="Train Booking API - Full Stack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trains.router, prefix="/api/v1/trains", tags=["trains"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["payments"])

@app.get("/")
async def root():
    return {
        "message": "🚂 Train Booking API - FULLY FUNCTIONAL!",
        "features": [
            "✅ View Trains", "✅ Search", "✅ Book Seats", 
            "✅ Login/Register", "✅ Payments", "✅ History"
        ],
        "endpoints": [
            "/api/v1/trains/", "/api/v1/bookings/", "/api/v1/users/login/"
        ]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
