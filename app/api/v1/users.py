from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas
from app.auth import authenticate_user, get_password_hash, create_access_token, USERS_DB
from datetime import timedelta  # ✅ FIXED!

router = APIRouter()

def init_demo_user():
    if not USERS_DB:
        USERS_DB.append({
            "user_id": 1,
            "email": "user@example.com",
            "hashed_password": get_password_hash("password123")
        })

@router.on_event("startup")
async def startup_event():
    init_demo_user()

@router.post("/login/", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)  # ✅ Now works!
    access_token = create_access_token(
        data={"sub": str(user["user_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register/")
async def register(user_data: schemas.UserCreate):
    if any(u["email"] == user_data.email for u in USERS_DB):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "user_id": len(USERS_DB) + 1,
        "email": user_data.email,
        "hashed_password": get_password_hash(user_data.password)
    }
    USERS_DB.append(new_user)
    return {"message": "User registered successfully", "user_id": new_user["user_id"]}
