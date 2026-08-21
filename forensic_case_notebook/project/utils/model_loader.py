"""
model_loader.py
----------------
Loads the trained EfficientNetB0 Keras model and caches it in memory so it
is only read from disk ONCE per app session (Streamlit reruns the whole
script on every user interaction, so caching is essential for performance).

This module is intentionally kept separate from app.py / predictor.py so
that the "how do I load my model" concern lives in exactly one place.
"""

import os
import streamlit as st
import tensorflow as tf

# Path to the trained model file (relative to project root).
# Swap this path if you rename your .keras file or move it elsewhere.
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "best_model_final.keras")


@st.cache_resource(show_spinner=False)
def load_trained_model():
    """
    Loads the trained .keras model from disk and caches the returned
    object across reruns / users of this app instance.

    IMPORTANT:
    - This app performs INFERENCE ONLY. The model is never re-trained,
      re-compiled for training, or modified in any way.
    - st.cache_resource is the correct Streamlit cache decorator for
      objects that cannot be pickled (like a TensorFlow/Keras model),
      as opposed to st.cache_data which is for serializable data.

    Returns
    -------
    tf.keras.Model
        The loaded, ready-to-use EfficientNetB0 classifier.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at '{MODEL_PATH}'.\n"
            "Make sure 'best_model_final.keras' is placed inside the "
            "'model/' folder before running or deploying the app."
        )

    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return model
