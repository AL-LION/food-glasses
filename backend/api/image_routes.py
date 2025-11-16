from fastapi import APIRouter, File, UploadFile
from PIL import Image                      # NEW
import numpy as np                         # NEW
from io import BytesIO                     # NEW

router = APIRouter()

# Endpoint for receiving an uploaded image and converting it to a NumPy array
@router.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    # Reject unsupported file types early
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Unsupported file type"}

    # Step 1: Load all bytes from the uploaded image
    img_bytes = await file.read()

    # Step 2: Convert image bytes → Pillow Image object (RGB)
    img = Image.open(BytesIO(img_bytes)).convert("RGB")

    # Step 3: Convert Pillow Image → NumPy array
    img_array = np.array(img)

    # Step 4: Extract metadata for debugging / testing
    height, width, channels = img_array.shape

    return {
        "message": "Image converted to NumPy array successfully",
        "filename": file.filename,
        "shape": img_array.shape,           # e.g. (1080, 720, 3)
        "height": int(height),
        "width": int(width),
        "channels": int(channels)
    }