from fastapi import APIRouter, HTTPException
from app import schemas

router = APIRouter()
PAYMENTS_DB = []

@router.post("/pay/")
def process_payment(payment: schemas.PaymentRequest):
    """Payment gateway integration"""
    if payment.booking_id > 10:  # Simulate invalid booking
        raise HTTPException(status_code=400, detail="Invalid booking ID")
    
    payment_record = {
        "payment_id": f"pay_{len(PAYMENTS_DB) + 1}",
        "booking_id": payment.booking_id,
        "amount": 2500.00,  # From booking
        "status": "succeeded",
        "timestamp": "2026-02-24T18:05:00"
    }
    
    PAYMENTS_DB.append(payment_record)
    return payment_record

@router.get("/status/{payment_id}/")
def payment_status(payment_id: str):
    """Check payment status"""
    payment = next((p for p in PAYMENTS_DB if p["payment_id"] == payment_id), None)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
