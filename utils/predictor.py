"""
predictor.py
------------
Handles image preprocessing and inference for the Saliva vs. Sweat
EfficientNetB0 TensorFlow Lite classifier.
"""

import numpy as np
from PIL import Image

# ------------------------------------------------------------
# MODEL CONFIGURATION
# ------------------------------------------------------------
IMG_SIZE = 224

# Model output mapping:
# 0 = Saliva
# 1 = Sweat
CLASS_NAMES = [
    "Saliva",
    "Sweat",
]


def preprocess_image(pil_image: Image.Image) -> np.ndarray:
    """
    Convert a PIL image into shape (1, 224, 224, 3).

    The original EfficientNetB0 model contains internal preprocessing,
    so pixel values are kept in the 0-255 range as float32.
    """

    # Ensure RGB
    image = pil_image.convert("RGB")

    # Resize to model input size
    image = image.resize((IMG_SIZE, IMG_SIZE))

    # Convert to numpy array
    array = np.asarray(image, dtype=np.float32)

    # Add batch dimension
    batch = np.expand_dims(array, axis=0)

    return batch


def predict_stain(interpreter, pil_image: Image.Image) -> dict:
    """
    Run inference using TensorFlow Lite.

    Returns:
        {
            "class": "Saliva",
            "confidence": 96.2,
            "probabilities": {
                "Saliva": 96.2,
                "Sweat": 3.8
            }
        }
    """

    batch = preprocess_image(pil_image)

    # Get model input/output information
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Match model input dtype
    input_dtype = input_details[0]["dtype"]
    batch = batch.astype(input_dtype)

    # Set input tensor
    interpreter.set_tensor(
        input_details[0]["index"],
        batch,
    )

    # Run model
    interpreter.invoke()

    # Get predictions
    raw_predictions = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    # Find class with highest probability
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
