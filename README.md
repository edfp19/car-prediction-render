# Car Price Cloud Architecture Showcase

This project demonstrates an end-to-end cloud deployment flow around a simple
scikit-learn regression model. The model predicts vehicle `MSRP`, but the main
deliverable is the deployment architecture: training, artifact creation, API
serving, a small frontend, Docker Compose, and a Render-ready container setup.

## Local Setup

```bash
uv sync
uv run python -m car_price.train
uv run uvicorn car_price.api:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` for the frontend.

## Docker Compose

```bash
docker compose up --build
```

The container trains the model on startup, saves the artifact to `models/`, and
then starts the API.

## API

Health check:

```bash
curl http://localhost:8000/health
```

Prediction:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "make": "bmw",
    "model": "1_series",
    "year": 2011,
    "engine_fuel_type": "premium_unleaded_(required)",
    "engine_hp": 300,
    "engine_cylinders": 6,
    "transmission_type": "manual",
    "driven_wheels": "rear_wheel_drive",
    "number_of_doors": 2,
    "market_category": "luxury,performance",
    "vehicle_size": "compact",
    "vehicle_style": "convertible",
    "highway_mpg": 28,
    "city_mpg": 19,
    "popularity": 3916
  }'
```

## Render Deployment

Use the Dockerfile as the web service runtime. The same startup command trains
the model and serves the API:

```bash
./scripts/start.sh
```

Set the service port to `8000` if Render does not infer it automatically.

## Architecture

```text
data/data.csv
    -> startup training with scikit-learn
    -> models/car_price_model.joblib
    -> FastAPI prediction service
    -> static frontend and JSON API
    -> Docker Compose locally
    -> Render web service
```
