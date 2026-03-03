import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import bookings, payments, trains, users

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
            "✅ View Trains",
            "✅ Search",
            "✅ Book Seats",
            "✅ Login/Register",
            "✅ Payments",
            "✅ History",
        ],
        "endpoints": ["/api/v1/trains/", "/api/v1/bookings/", "/api/v1/users/login/"],
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/nithish-cd-test")
async def cd_test():
    return {"cd": "Working", "deployed": "03/03/2026"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ✅ Render default
    uvicorn.run(app, host="0.0.0.0", port=port)
