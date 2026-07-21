# Demo de arquitectura cloud para prediccion de precios

Este proyecto muestra un flujo de despliegue end-to-end alrededor de un modelo
simple de regresion con scikit-learn. El modelo predice el `MSRP` de un vehiculo,
pero el entregable principal es la arquitectura de despliegue: entrenamiento,
creacion del artefacto, API, interfaz web pequena, Docker Compose y preparacion para
Render.

## Configuracion local

```bash
uv sync
uv run python -m car_price.train
uv run uvicorn car_price.api:app --host 0.0.0.0 --port 8000
```

Abre `http://localhost:8000` para usar la interfaz web.

## Docker Compose

```bash
docker compose up --build
```

El contenedor entrena el modelo al iniciar, guarda el artefacto en `models/` y
despues levanta la API.

## API

Revision de salud:

```bash
curl http://localhost:8000/health
```

Prediccion:

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

Opciones para los dropdowns:

```bash
curl http://localhost:8000/options
```

## Despliegue en Render

Usa el `Dockerfile` como runtime del servicio web. El mismo comando de arranque
entrena el modelo y sirve la API:

```bash
./scripts/start.sh
```

Configura el puerto del servicio como `8000` si Render no lo detecta
automaticamente.

## Arquitectura

```text
data/data.csv
    -> entrenamiento al iniciar con scikit-learn
    -> models/car_price_model.joblib
    -> servicio de prediccion con FastAPI
    -> interfaz web estatica y API JSON
    -> Docker Compose en local
    -> servicio web en Render
```
