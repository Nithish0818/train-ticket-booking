from fastapi import APIRouter, HTTPException
from typing import List
from app import schemas, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.Train])
def view_trains_schedule(skip: int = 0, limit: int = 100):
    trains = crud.get_trains(None, skip=skip, limit=limit)
    return trains

@router.get("/search/")
def search_trains(from_station: str, to_station: str, date: str):
    trains = crud.search_trains(from_station, to_station, date, None)
    if not trains:
        raise HTTPException(status_code=404, detail="No trains found")
    return {"trains": trains, "count": len(trains)}

@router.get("/{train_id}/seats/")
def check_seats(train_id: int):
    seats = crud.check_seats(train_id, None)
    return {"train_id": train_id, "available_seats": seats}

@router.get("/{train_id}/fare/")
def fare_enquiry(train_id: int):
    trains = crud.load_sample_trains()
    train = next((t for t in trains if t.train_id == train_id), None)
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return {"train_id": train_id, "fare": train.fare}
