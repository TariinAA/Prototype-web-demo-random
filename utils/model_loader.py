"""
model_loader.py
----------------
Loads the trained TensorFlow Lite model and caches the interpreter
so it is only initialized once per Streamlit app session.
"""

import os
import streamlit as st
from tflite_runtime.interpreter import Interpreter

# Path to the TFLite model file
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "model",
    "best_model_final.tflite"
)


@st.cache_resource(show_spinner=False)
def load_trained_model():
    """
    Loads the trained TFLite model and prepares the interpreter.

    Returns
    -------
    Interpreter
        Ready-to-use TensorFlow Lite interpreter.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at '{MODEL_PATH}'.\n"
            "Make sure 'best_model_final.tflite' is placed inside "
            "the 'model/' folder."
        )

    interpreter = Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()

    return interpreter
