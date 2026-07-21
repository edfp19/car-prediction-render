from pathlib import Path

DATA_PATH = Path("data/data.csv")
MODEL_PATH = Path("models/car_price_model.joblib")

RAW_TARGET = "MSRP"

COLUMN_MAP = {
    "Make": "make",
    "Model": "model",
    "Year": "year",
    "Engine Fuel Type": "engine_fuel_type",
    "Engine HP": "engine_hp",
    "Engine Cylinders": "engine_cylinders",
    "Transmission Type": "transmission_type",
    "Driven_Wheels": "driven_wheels",
    "Number of Doors": "number_of_doors",
    "Market Category": "market_category",
    "Vehicle Size": "vehicle_size",
    "Vehicle Style": "vehicle_style",
    "highway MPG": "highway_mpg",
    "city mpg": "city_mpg",
    "Popularity": "popularity",
    "MSRP": "msrp",
}

FEATURES = [
    "make",
    "model",
    "year",
    "engine_fuel_type",
    "engine_hp",
    "engine_cylinders",
    "transmission_type",
    "driven_wheels",
    "number_of_doors",
    "market_category",
    "vehicle_size",
    "vehicle_style",
    "highway_mpg",
    "city_mpg",
    "popularity",
]

BASE_NUMERIC_FEATURES = [
    "engine_hp",
    "engine_cylinders",
    "highway_mpg",
    "city_mpg",
    "popularity",
]

NUMERIC_FEATURES = [
    "engine_hp",
    "engine_cylinders",
    "highway_mpg",
    "city_mpg",
    "popularity",
    "age",
]

CATEGORICAL_FEATURES = [
    "make",
    "model",
    "engine_fuel_type",
    "driven_wheels",
    "market_category",
    "vehicle_size",
    "vehicle_style",
]

DOOR_VALUES = [2, 3, 4]
REFERENCE_YEAR = 2017
TOP_CATEGORY_VALUES = 5
