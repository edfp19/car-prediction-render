#!/usr/bin/env bash
set -euo pipefail

uv run python -m car_price.train
uv run uvicorn car_price.api:app --host 0.0.0.0 --port "${PORT:-8000}"
