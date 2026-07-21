from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from car_price.config import FEATURES, MODEL_PATH
from car_price.train import prepare_features


@lru_cache(maxsize=1)
def load_model(model_path: str | None = None) -> dict[str, Any]:
    path = Path(model_path or os.getenv("MODEL_PATH", MODEL_PATH))
    return joblib.load(path)


def predict_price(car: dict[str, Any]) -> float:
    artifact = load_model()
    row = pd.DataFrame([{feature: car.get(feature) for feature in FEATURES}])
    for column in row.select_dtypes(include="object").columns:
        row[column] = row[column].str.lower().str.replace(" ", "_")
    X = prepare_features(row, artifact["categorical_values"])
    log_prediction = artifact["pipeline"].predict(X)[0]
    return float(np.expm1(log_prediction))


def prediction_options() -> dict[str, list[str]]:
    artifact = load_model()
    options = artifact["categorical_values"].copy()
    options["transmission_type"] = ["automatic", "manual", "automated_manual", "direct_drive", "unknown"]
    options["number_of_doors"] = ["2", "3", "4"]
    return options
