from fastapi import APIRouter, File, UploadFile
from PIL import Image
from io import BytesIO

# Correct import based on your folder structure
from backend.models.product_classifier import classify_image

router = APIRouter()

@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    """
    Receive an uploaded image, run ONNX produce classification,
    and return the predicted label and confidence.
    """

    # Only accept JPEG or PNG
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Unsupported file type"}

    # Read binary content
    img_bytes = await file.read()

    # Convert to Pillow image
    try:
        pil_image = Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception:
        return {"error": "Unable to read image"}

    # Run classifier
    try:
        prediction = classify_image(pil_image)
    except Exception as e:
        return {"error": f"Model inference failed: {str(e)}"}

    # Respond with result
    return {
        "filename": file.filename,
        "predicted_item": prediction["label"],
        "confidence": prediction["confidence"],
        "class_index": prediction["index"]
    }
