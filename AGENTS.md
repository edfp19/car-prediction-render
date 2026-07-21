# AGENTS.md

## Intencion del proyecto

Este proyecto es una demo de arquitectura cloud que usa un modelo pequeno de
machine learning como carga de trabajo. El modelo no es el producto; el producto
es una historia de despliegue end-to-end clara, reproducible y facil de explicar:

1. Entrenar un modelo de regresion con scikit-learn usando datos locales.
2. Guardar el artefacto entrenado.
3. Servir predicciones mediante una API pequena.
4. Ejecutar toda la aplicacion con un solo archivo Docker Compose.
5. Desplegar el servicio en Render.
6. Documentar el flujo local-a-cloud para una presentacion de clase.

## Estilo de referencia

Usa el estilo didactico y simple de DataTalksClub Machine Learning Zoomcamp
`02-regression`: scripts legibles, pandas/scikit-learn directo, validacion
explicita, reporte de RMSE y guardado del artefacto. Mantener la implementacion
entendible es mas importante que usar una arquitectura compleja.

## Estructura propuesta

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

## Guia de implementacion

- Usar `uv` como gestor de paquetes de Python.
- Mantener las dependencias en `pyproject.toml`.
- Preferir pipelines simples de scikit-learn para preparacion y modelado.
- El entrenamiento debe poder ejecutarse con `uv run python -m car_price.train`.
- El servicio debe poder ejecutarse con `uv run uvicorn car_price.api:app --host 0.0.0.0 --port 8000`.
- Guardar los artefactos generados bajo `models/`.
- No commitear binarios generados del modelo, caches, entornos virtuales o secretos locales.
- Usar Docker Compose como punto de entrada del despliegue.
- Usar variables de entorno para configuracion de runtime, como ruta del modelo y puerto.
- Mantener los tests enfocados en carga del artefacto, forma de la prediccion y comportamiento basico de la API.

## Requisitos de la demo de despliegue

El proyecto final debe incluir:

- Un comando local de entrenamiento.
- Un comando local para levantar la API.
- Un `compose.yaml` que construya y sirva la API.
- Una ruta de despliegue en Render usando el mismo contrato de contenedor cuando sea posible.
- Una seccion del README con comandos o evidencia de que el endpoint desplegado responde.
- Una explicacion corta de arquitectura apropiada para una clase de arquitectura cloud.

## Decisiones confirmadas

- El target de prediccion es `MSRP`, normalizado como `msrp` en el codigo de entrenamiento.
- `data/data.csv` debe commitearse porque forma parte de la reproducibilidad del proyecto.
- Incluir una interfaz web pequena dentro del mismo servicio FastAPI.
- Entrenar el modelo al iniciar el contenedor antes de servir la API.
- Mantener el modelo simple y basado en scikit-learn.
