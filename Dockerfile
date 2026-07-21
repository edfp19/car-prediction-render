FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV MODEL_PATH=/app/models/car_price_model.joblib
ENV DATA_PATH=/app/data/data.csv
ENV PORT=8000

COPY pyproject.toml ./
RUN uv sync --no-dev

COPY . .
RUN chmod +x ./scripts/start.sh

EXPOSE 8000

CMD ["./scripts/start.sh"]
