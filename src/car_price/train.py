from __future__ import annotations

import os
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error
from sklearn.pipeline import Pipeline

from car_price.config import (
    BASE_NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    COLUMN_MAP,
    DATA_PATH,
    DOOR_VALUES,
    FEATURES,
    MODEL_PATH,
    REFERENCE_YEAR,
    TOP_CATEGORY_VALUES,
)


def read_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns=COLUMN_MAP)
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    string_columns = list(df.dtypes[df.dtypes == "object"].index)
    for column in string_columns:
        df[column] = df[column].str.lower().str.replace(" ", "_")
    return df


def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    n = len(df)
    n_val = int(n * 0.2)
    n_test = int(n * 0.2)
    n_train = n - n_val - n_test

    idx = np.arange(n)
    np.random.seed(2)
    np.random.shuffle(idx)

    df_train = df.iloc[idx[:n_train]].reset_index(drop=True)
    df_val = df.iloc[idx[n_train : n_train + n_val]].reset_index(drop=True)
    df_test = df.iloc[idx[n_train + n_val :]].reset_index(drop=True)

    return df_train, df_val, df_test


def get_top_categories(df_train: pd.DataFrame) -> dict[str, list[str]]:
    return {
        column: list(df_train[column].value_counts().head(TOP_CATEGORY_VALUES).index)
        for column in CATEGORICAL_FEATURES
    }


def prepare_features(df: pd.DataFrame, categorical_values: dict[str, list[str]]) -> pd.DataFrame:
    df = df.copy()
    df["age"] = REFERENCE_YEAR - df["year"]

    engineered_features = BASE_NUMERIC_FEATURES + ["age"]

    for value in DOOR_VALUES:
        column = f"num_doors_{value}"
        df[column] = (df["number_of_doors"] == value).astype(int)
        engineered_features.append(column)

    for column, values in categorical_values.items():
        for value in values:
            feature = f"{column}_{value}"
            df[feature] = (df[column] == value).astype(int)
            engineered_features.append(feature)

    return df[engineered_features].fillna(0)


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value=0)),
            ("model", Ridge(alpha=0.001, solver="lsqr")),
        ]
    )


def train(data_path: Path = DATA_PATH, model_path: Path = MODEL_PATH) -> dict[str, float]:
    df = read_data(data_path)
    df_train, df_val, df_test = split_data(df)

    y_train = np.log1p(df_train["msrp"].values)
    y_val = np.log1p(df_val["msrp"].values)
    y_test = np.log1p(df_test["msrp"].values)

    categorical_values = get_top_categories(df_train)
    X_train = prepare_features(df_train.drop(columns=["msrp"]), categorical_values)
    X_val = prepare_features(df_val.drop(columns=["msrp"]), categorical_values)

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_val)
    val_rmse = root_mean_squared_error(y_val, y_pred)

    df_full_train = pd.concat([df_train, df_val]).reset_index(drop=True)
    y_full_train = np.concatenate([y_train, y_val])
    X_full_train = prepare_features(df_full_train.drop(columns=["msrp"]), categorical_values)
    X_test = prepare_features(df_test.drop(columns=["msrp"]), categorical_values)

    pipeline.fit(X_full_train, y_full_train)
    test_rmse = root_mean_squared_error(y_test, pipeline.predict(X_test))

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "pipeline": pipeline,
            "features": FEATURES,
            "categorical_values": categorical_values,
            "val_rmse_log_price": val_rmse,
            "test_rmse_log_price": test_rmse,
        },
        model_path,
    )

    return {
        "val_rmse_log_price": float(val_rmse),
        "test_rmse_log_price": float(test_rmse),
    }


def main() -> None:
    data_path = Path(os.getenv("DATA_PATH", DATA_PATH))
    model_path = Path(os.getenv("MODEL_PATH", MODEL_PATH))
    metrics = train(data_path=data_path, model_path=model_path)
    print(f"saved model to {model_path}")
    print(f"validation rmse on log(msrp): {metrics['val_rmse_log_price']:.4f}")
    print(f"test rmse on log(msrp): {metrics['test_rmse_log_price']:.4f}")


if __name__ == "__main__":
    main()
