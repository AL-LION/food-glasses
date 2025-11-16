from fastapi import APIRouter, File, UploadFile
from PIL import Image
from io import BytesIO
import numpy as np     # <-- NEW

from backend.models.product_classifier import classify_image
from backend.data.loader import FOODS

# NEW: import your heuristics from the spoilage package
from backend.utils.spoilage import (
    detect_dark_patches,
    detect_mold,
    detect_shrivel
)

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Receive an uploaded image, run ONNX produce classification,
    return predicted label, confidence, spoilage info, and detected issues.
    """

    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Unsupported file type"}

    img_bytes = await file.read()

    try:
        pil_image = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception:
        return {"error": "Unable to read image"}

    # Convert PIL → numpy array for heuristics
    np_image = np.array(pil_image)

    # Run ONNX model
    try:
        prediction = classify_image(pil_image)
    except Exception as e:
        return {"error": f"Model inference failed: {str(e)}"}

    # ---------------------------
    # NEW: Spoilage Issue Heuristics (Phase 4)
    # ---------------------------
    issues = []
    issues += detect_dark_patches(np_image)
    issues += detect_mold(np_image)
    issues += detect_shrivel(np_image)

    # ---------------------------
    # Lookup spoilage info
    # ---------------------------
    label_lower = prediction["label"].lower()
    spoilage = next((item for item in FOODS if item["name"] == label_lower), None)

    if spoilage is None:
        return {
            "filename": file.filename,
            "predicted_item": prediction["label"],
            "confidence": prediction["confidence"],
            "class_index": prediction["index"],
            "issues": issues,        # <-- NEW
            "spoilage_info": None,
            "error": "Item not found in spoilage database",
        }

    # ---------------------------
    # Final combined response
    # ---------------------------
    return {
        "filename": file.filename,
        "predicted_item": prediction["label"],
        "confidence": prediction["confidence"],
        "class_index": prediction["index"],
        "issues": issues,          # <-- NEW
        "spoilage_info": spoilage,
    }
