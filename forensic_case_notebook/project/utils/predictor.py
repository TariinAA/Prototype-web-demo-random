"""
predictor.py
------------
Handles image preprocessing and inference for the Saliva vs. Sweat
EfficientNetB0 classifier.

Kept separate from app.py so the UI code never has to know anything
about tensors, resizing, or model internals.
"""

import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# MODEL CONFIGURATION
# Edit these two values if you retrain the model with a different image
# size or a different (or reordered) set of class labels.
# ---------------------------------------------------------------------------
IMG_SIZE = 224

# Model output mapping:
# 0 = Saliva
# 1 = Sweat
# NOTE: Order matters! This MUST match the class index order used during
# training (e.g. the alphabetical folder order Keras' flow_from_directory /
# image_dataset_from_directory assigns: index 0 -> first folder name,
# index 1 -> second folder name, ...).
CLASS_NAMES = [
    "Saliva",  # index 0
    "Sweat"    # index 1
]


def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    """
    Converts a PIL image into a model-ready batch of shape (1, 224, 224, 3).

    เปลี่ยน preprocessing ให้ตรงกับ preprocessing ตอน Train Model
    (Change this preprocessing to match exactly what was used at train time.)

    This model was inspected directly from its saved config and its first
    two layers after the input layer are Keras' built-in `Rescaling` and
    `Normalization` layers (the standard `keras.applications.EfficientNetB0`
    preprocessing stack). That means the model expects RAW pixel values in
    the 0-255 range as float32 -- it rescales/normalizes internally, so we
    deliberately do NOT divide by 255 here. If you retrain the model with a
    different preprocessing pipeline (e.g. manual /255.0, or
    `efficientnet.preprocess_input`), update this function to match.
    """
    # Ensure 3 color channels (handles grayscale / RGBA uploads safely)
    image = pil_image.convert("RGB")

    # Resize to the size the model was trained on
    image = image.resize((IMG_SIZE, IMG_SIZE))

    # PIL -> numpy array, keep raw 0-255 float32 values (see note above)
    array = np.asarray(image).astype("float32")

    # Add batch dimension: (224, 224, 3) -> (1, 224, 224, 3)
    batch = np.expand_dims(array, axis=0)
    return batch


def predict_stain(model, pil_image: Image.Image) -> dict:
    """
    Runs a single image through the model and returns a clean result dict.

    Returns
    -------
    dict with keys:
        "class"        -> str, the predicted class name (e.g. "Saliva")
        "confidence"   -> float, confidence of the predicted class as a
                           percentage rounded to 1 decimal (e.g. 96.2)
        "probabilities"-> dict[str, float], every class -> its confidence %
                           (useful for showing a full breakdown / chart)
    """
    batch = preprocess_image(pil_image)
    raw_predictions = model.predict(batch, verbose=0)[0]  # shape: (num_classes,)

    predicted_index = int(np.argmax(raw_predictions))
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(raw_predictions[predicted_index]) * 100.0

    probabilities = {
        CLASS_NAMES[i]: round(float(raw_predictions[i]) * 100.0, 1)
        for i in range(len(CLASS_NAMES))
    }

    return {
        "class": predicted_class,
        "confidence": round(confidence, 1),
        "probabilities": probabilities,
    }
