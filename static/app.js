const form = document.querySelector("#predict-form");
const result = document.querySelector("#result");

const messages = {
  es: {
    eyebrow: "Demo para clase de arquitectura cloud",
    title: "Servicio de prediccion de MSRP",
    summary:
      "Un modelo de scikit-learn se entrena al iniciar el contenedor, guarda un artefacto y sirve predicciones con FastAPI.",
    make: "Marca",
    model: "Modelo",
    year: "Ano",
    engineHp: "Potencia del motor",
    engineCylinders: "Cilindros",
    transmission: "Transmision",
    drivenWheels: "Traccion",
    vehicleSize: "Tamano",
    vehicleStyle: "Estilo",
    fuelType: "Combustible",
    marketCategory: "Categoria",
    doors: "Puertas",
    highwayMpg: "MPG carretera",
    cityMpg: "MPG ciudad",
    popularity: "Popularidad",
    submit: "Predecir MSRP",
    waiting: "Esperando prediccion",
    predicting: "Calculando...",
    failed: "No se pudo calcular la prediccion",
    predicted: "MSRP estimado",
  },
  en: {
    eyebrow: "Cloud architecture class demo",
    title: "Car MSRP Prediction Service",
    summary:
      "A scikit-learn model trains on container startup, saves an artifact, and serves predictions through FastAPI.",
    make: "Make",
    model: "Model",
    year: "Year",
    engineHp: "Engine HP",
    engineCylinders: "Engine cylinders",
    transmission: "Transmission",
    drivenWheels: "Driven wheels",
    vehicleSize: "Vehicle size",
    vehicleStyle: "Vehicle style",
    fuelType: "Fuel type",
    marketCategory: "Market category",
    doors: "Doors",
    highwayMpg: "Highway MPG",
    cityMpg: "City MPG",
    popularity: "Popularity",
    submit: "Predict MSRP",
    waiting: "Awaiting prediction",
    predicting: "Predicting...",
    failed: "Prediction failed",
    predicted: "Predicted MSRP",
  },
};

const language = navigator.language.toLowerCase().startsWith("en") ? "en" : "es";
const copy = messages[language];

const numericFields = new Set([
  "year",
  "engine_hp",
  "engine_cylinders",
  "number_of_doors",
  "highway_mpg",
  "city_mpg",
  "popularity",
]);

function applyLanguage() {
  document.documentElement.lang = language;
  document.title =
    language === "en"
      ? "Car Price Deployment Showcase"
      : "Demo de despliegue para prediccion de precios";

  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = copy[element.dataset.i18n];
  });
}

function prettifyOption(value) {
  return value.replaceAll("_", " ");
}

function setSelectOptions(select, values) {
  const defaultValue = select.dataset.default;
  const uniqueValues = [...new Set([defaultValue, ...values].filter(Boolean))];

  select.innerHTML = "";
  uniqueValues.forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = prettifyOption(value);
    select.append(option);
  });
  select.value = defaultValue;
}

async function loadOptions() {
  const fallbackOptions = {
    make: ["bmw", "toyota", "volkswagen", "ford", "chevrolet"],
    model: ["1_series", "sienna", "silverado_1500", "tundra", "f-150"],
    engine_fuel_type: ["regular_unleaded", "premium_unleaded_(required)"],
    transmission_type: ["automatic", "manual", "automated_manual", "direct_drive", "unknown"],
    driven_wheels: ["front_wheel_drive", "rear_wheel_drive", "all_wheel_drive", "four_wheel_drive"],
    market_category: ["crossover", "flex_fuel", "luxury", "performance", "hatchback"],
    vehicle_size: ["compact", "midsize", "large"],
    vehicle_style: ["sedan", "4dr_suv", "coupe", "convertible", "passenger_minivan"],
    number_of_doors: ["2", "3", "4"],
  };

  let options = fallbackOptions;
  try {
    const response = await fetch("/options");
    if (response.ok) {
      options = { ...fallbackOptions, ...(await response.json()) };
    }
  } catch {
    options = fallbackOptions;
  }

  form.querySelectorAll("select").forEach((select) => {
    setSelectOptions(select, options[select.name] || []);
  });
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.textContent = copy.predicting;

  const payload = {};
  for (const [key, value] of new FormData(form).entries()) {
    payload[key] = numericFields.has(key) ? Number(value) : value;
  }

  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    result.textContent = copy.failed;
    return;
  }

  const data = await response.json();
  result.textContent = `${copy.predicted}: $${data.predicted_msrp.toLocaleString()}`;
});

applyLanguage();
loadOptions();
