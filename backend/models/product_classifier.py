import numpy as np
from PIL import Image
import onnxruntime as ort
import os

# ---------------------------------------------------------
# Paths to ONNX model + labels
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(__file__)  # backend/models/

MODEL_PATH = os.path.join(BASE_DIR, "fruit_classifier.onnx")
LABELS_PATH = os.path.join(BASE_DIR, "fruit_labels.txt")

# ---------------------------------------------------------
# Load Labels
# ---------------------------------------------------------

if not os.path.exists(LABELS_PATH):
    raise FileNotFoundError(f"Labels file not found at {LABELS_PATH}")

with open(LABELS_PATH, "r", encoding="utf-8") as f:
    LABELS = [line.strip() for line in f if line.strip()]

# ---------------------------------------------------------
# Load ONNX Model
# ---------------------------------------------------------

session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
INPUT_SIZE = 224  # EfficientNet input size

# ---------------------------------------------------------
# Preprocessing (EfficientNet ImageNet style)
# ---------------------------------------------------------

MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    image = image.resize((INPUT_SIZE, INPUT_SIZE))

    img = np.array(image).astype(np.float32) / 255.0  # HWC
    img = (img - MEAN) / STD  # normalize

    img = np.transpose(img, (2, 0, 1))  # HWC → CHW
    img = np.expand_dims(img, 0)        # Add batch dim

    return img

# ---------------------------------------------------------
# Classifier Function
# ---------------------------------------------------------

def classify_image(image: Image.Image) -> dict:
    input_tensor = preprocess_image(image)
    outputs = session.run(None, {input_name: input_tensor})
    logits = outputs[0][0]

    exp = np.exp(logits - np.max(logits))
    probs = exp / exp.sum()

    idx = int(np.argmax(probs))

    return {
        "label": LABELS[idx] if 0 <= idx < len(LABELS) else "unknown",
        "confidence": float(probs[idx]),
        "index": idx
    }
