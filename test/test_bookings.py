import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import USERS_DB, get_password_hash

client = TestClient(app)

def test_create_booking():
    # 🔥 EXACT MATCH - All 3 required fields from your code
    hashed_pw = get_password_hash("password123")
    USERS_DB.insert(0, {
        "user_id": 1,              # ✅ Fixes users.py:29 KeyError
        "email": "testuser@test.com",  # ✅ Matches auth.py:73
        "username": "testuser",        # ✅ Login field
        "hashed_password": hashed_pw   # ✅ Password verification
    })
    
    print(f"🔍 Created test user: {USERS_DB[0]}")
    
    login_data = {"username": "testuser@test.com", "password": "password123"}
    login_response = client.post("/api/v1/users/login", data=login_data)
    
    print(f"Login status: {login_response.status_code}")
    print(f"Login response: {login_response.json()}")
    
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Booking test
    booking_data = {"train_id": 1, "passenger_name": "Nithish", "seats": 2}
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/api/v1/bookings", json=booking_data, headers=headers)
    assert response.status_code == 200  # ✅ Your endpoint returns 200
    assert "booking_id" in response.json()
    print(f"✅ Booking: {response.json()}")