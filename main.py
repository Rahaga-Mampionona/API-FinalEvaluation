from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

@app.get("/ping", response_model=str)
def ping():
    return "pong"

class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic



cars_db: Dict[str, Car] = {}

@app.post("/cars", status_code=status.HTTP_201_CREATED, response_model=Car)
def create_car(car: Car):
    if car.identifier in cars_db:
        raise HTTPException(status_code=400, detail="Car avec cet ID existe déjà")
    cars_db[car.identifier] = car
    return car

@app.get("/cars", response_model=List[Car])
def get_cars():
    return list(cars_db.values())


@app.get("/cars/{id}", response_model=Car)
def get_car(id: str):
    if id not in cars_db:
        raise HTTPException(
            status_code=404,
            detail=f"Car avec id {id} n'existe pas",
        )
    return cars_db[id]

@app.put("/cars/{id}/characteristics", response_model=Car)
def update_characteristics(id: str, new_char: Characteristic):
    if id not in cars_db:
        raise HTTPException(
            status_code=404,
            detail=f"Car avec id {id} introuvable"
        )

    car = cars_db[id]
    car.characteristics = new_char
    cars_db[id] = car
    return car
