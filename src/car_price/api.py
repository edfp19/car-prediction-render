from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from car_price.predict import predict_price, prediction_options

app = FastAPI(title="Car Price Cloud Architecture Showcase")
app.mount("/static", StaticFiles(directory="static"), name="static")


class CarFeatures(BaseModel):
    make: str = "bmw"
    model: str = "1_series"
    year: int = 2011
    engine_fuel_type: str = "premium_unleaded_(required)"
    engine_hp: float = 300
    engine_cylinders: float = 6
    transmission_type: str = "manual"
    driven_wheels: str = "rear_wheel_drive"
    number_of_doors: float = 2
    market_category: str = "luxury,performance"
    vehicle_size: str = "compact"
    vehicle_style: str = "convertible"
    highway_mpg: float = Field(default=28, alias="highway_mpg")
    city_mpg: float = Field(default=19, alias="city_mpg")
    popularity: float = 3916


@app.get("/")
def index() -> FileResponse:
    return FileResponse("static/index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/options")
def options() -> dict[str, list[str]]:
    return prediction_options()


@app.post("/predict")
def predict(car: CarFeatures) -> dict[str, float]:
    prediction = predict_price(car.model_dump())
    return {"predicted_msrp": round(prediction, 2)}
