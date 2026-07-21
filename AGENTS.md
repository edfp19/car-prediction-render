# AGENTS.md

## Project Intent

This is a cloud architecture showcase that uses a small machine learning model as the workload. The model is not the product; the product is a clear, reproducible end-to-end deployment story:

1. Train a scikit-learn regression model from local data.
2. Save the trained artifact.
3. Serve predictions through a small API.
4. Run the whole application with one Docker Compose file.
5. Deploy the compose-based service on Render.
6. Document the local-to-cloud workflow clearly enough for a class presentation.

## Reference Style

Use the simple teaching style from DataTalksClub Machine Learning Zoomcamp `02-regression`: readable scripts, straightforward pandas/scikit-learn training, explicit validation, RMSE reporting, and a saved model artifact. Keep the implementation approachable rather than framework-heavy.

## Proposed Folder Structure

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── compose.yaml
├── Dockerfile
├── data/
│   └── data.csv
├── models/
│   └── .gitkeep
├── notebooks/
│   └── exploration.ipynb
├── src/
│   └── car_price/
│       ├── __init__.py
│       ├── config.py
│       ├── train.py
│       ├── predict.py
│       └── api.py
└── tests/
    ├── test_predict.py
    └── test_api.py
```

## Implementation Guidelines

- Use `uv` as the Python package manager.
- Keep dependencies in `pyproject.toml`.
- Prefer simple scikit-learn pipelines for preprocessing and modeling.
- Keep training code runnable with `uv run python -m car_price.train`.
- Keep serving code runnable with `uv run uvicorn car_price.api:app --host 0.0.0.0 --port 8000`.
- Save generated model artifacts under `models/`.
- Do not commit generated model binaries, caches, virtual environments, or local secrets.
- Keep Docker Compose as the deployment entry point.
- Use environment variables for runtime settings such as model path and port.
- Keep tests focused on artifact loading, prediction shape, and API health/prediction behavior.

## Deployment Showcase Requirements

The final project should include:

- A local training command.
- A local API command.
- A `compose.yaml` that builds and serves the API.
- A Render deployment path using the same container/compose contract where possible.
- A README section with screenshots or command output showing the deployed endpoint responding.
- A short architecture explanation suitable for a cloud architecture class.

## Confirmed Decisions

- The prediction target is `MSRP`, normalized to `msrp` in training code.
- Commit `data/data.csv`; it is part of the reproducible class project.
- Include a small frontend in the same FastAPI service.
- Train the model on container startup before serving the API.
- Keep the model implementation simple and scikit-learn based.
