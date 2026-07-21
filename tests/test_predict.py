from pathlib import Path

import pandas as pd

from car_price.train import train


def test_train_writes_model(tmp_path: Path) -> None:
    data_path = tmp_path / "sample.csv"
    model_path = tmp_path / "model.joblib"
    df = pd.read_csv("data/data.csv").sample(n=120, random_state=2)
    df.to_csv(data_path, index=False)

    metrics = train(data_path=data_path, model_path=model_path)

    assert model_path.exists()
    assert metrics["val_rmse_log_price"] > 0
    assert metrics["test_rmse_log_price"] > 0
