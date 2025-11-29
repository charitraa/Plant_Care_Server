# ml_image_loader.py
import os
import numpy as np
from tensorflow.keras.models import load_model # pyright: ignore[reportMissingImports]
from tensorflow.keras.preprocessing.image import load_img, img_to_array # pyright: ignore[reportMissingImports]
from django.conf import settings

# Path to your trained Keras model
MODEL_PATH = os.path.join(settings.BASE_DIR, "models", "plant_classifier.h5")

# Load model once when server starts
model = load_model(MODEL_PATH)

# Class names in the same order as training
classes = ['Aloe Vera', 'Snake Plant']

def predict_plant_type(image_path):
    """
    Takes path to image file, returns predicted class and confidence
    """
    # Load & preprocess image
    img = load_img(image_path, target_size=(128, 128))  # resize to same as training
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # normalize

    # Predict
    prediction = model.predict(img_array)[0][0]
    predicted_class = classes[1] if prediction > 0.5 else classes[0]
    confidence = prediction if prediction > 0.5 else 1 - prediction
    return predicted_class, confidence