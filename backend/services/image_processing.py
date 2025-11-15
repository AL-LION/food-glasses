from io import BytesIO
from PIL import Image

async def analyze_image(uploaded_file):
    contents = await uploaded_file.read()

    # Load the image to validate the upload works
    try:
        Image.open(BytesIO(contents)).convert("RGB")
    except Exception:
        return {"error": "Invalid image"}

    # Placeholder output for Phase 1
    return {
        "message": "Image received successfully (Phase 1 stub).",
        "filename": uploaded_file.filename
    }
