from fastapi import APIRouter, File, UploadFile
from PIL import Image
from io import BytesIO

from backend.models.product_classifier import classify_image
from backend.data.loader import FOODS   # <-- NEW

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Receive an uploaded image, run ONNX produce classification,
    and return the predicted label, confidence, and spoilage info.
    """

    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Unsupported file type"}

    img_bytes = await file.read()

    try:
        pil_image = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception:
        return {"error": "Unable to read image"}

    try:
        prediction = classify_image(pil_image)
    except Exception as e:
        return {"error": f"Model inference failed: {str(e)}"}

    # ---------------------------
    # NEW: Lookup spoilage info
    # ---------------------------
    label_lower = prediction["label"].lower()
    spoilage = next((item for item in FOODS if item["name"] == label_lower), None)

    if spoilage is None:
        return {
            "filename": file.filename,
            "predicted_item": prediction["label"],
            "confidence": prediction["confidence"],
            "class_index": prediction["index"],
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
        "spoilage_info": spoilage,
    }
