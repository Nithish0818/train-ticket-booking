from datetime import datetime
from app import schemas

def load_sample_trains():
    return [
        schemas.Train(
            train_id=1, train_name="Chennai Express", from_station="MAS",
            to_station="HYB", departure_time="2026-02-25T18:30:00",
            arrival_time="2026-02-26T06:45:00", total_seats=100,
            available_seats=85, fare=1250.00
        ),
        schemas.Train(
            train_id=2, train_name="Mumbai Mail", from_station="MAS",
            to_station="BCT", departure_time="2026-02-25T22:15:00",
            arrival_time="2026-02-26T20:30:00", total_seats=120,
            available_seats=92, fare=1850.00
        )
    ]

def get_trains(db, skip=0, limit=100):
    trains = load_sample_trains()
    return trains[skip:skip + limit]

def search_trains(from_station: str, to_station: str, date: str, db):
    all_trains = load_sample_trains()
    return [t for t in all_trains 
            if t.from_station == from_station and t.to_station == to_station]

def check_seats(train_id: int, db):
    trains = load_sample_trains()
    train = next((t for t in trains if t.train_id == train_id), None)
    return train.available_seats if train else 0
