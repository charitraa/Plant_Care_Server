import os
import joblib
import numpy as np
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "models", "watering_reminder_model.pkl")
# Map plant types to integers
PLANT_TYPE_MAPPING = {
    "Aloe Vera": 1,
    "Snake Plant": 2,
}

try:
    pipeline = joblib.load(MODEL_PATH)
except Exception as e:
    pipeline = None
    print(f"Failed to load watering model: {e}")

def predict_watering_days(plant_type, temperature, humidity, sunlight, days_since_watered=0):
    if pipeline is None:
        raise RuntimeError("Watering model not loaded")

    # Convert plant_type string to numeric ID
    plant_type_num = PLANT_TYPE_MAPPING.get(plant_type)
    if plant_type_num is None:
        raise ValueError(f"Unknown plant type: {plant_type}")

    X = np.array([[plant_type_num, float(temperature), float(humidity), float(sunlight), float(days_since_watered)]])
    pred = pipeline.predict(X)[0]
    return round(pred, 2)

