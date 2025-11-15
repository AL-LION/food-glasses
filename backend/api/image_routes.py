from fastapi import APIRouter, UploadFile, File
from services.image_processing import analyze_image

router = APIRouter(
    prefix="/api",
    tags=["Image Analysis"]
)

@router.get("/ping")
async def ping():
    return {"message": "backend alive"}

@router.post("/analyze-image")
async def analyze_image_route(file: UploadFile = File(...)):
    return await analyze_image(file)

@router.post("/analyze-food")
async def analyze_food(food_name: str = "unknown"):
    return {
        "food": food_name,
        "message": "Food analysis placeholder (Phase 1). Real logic comes in Phase 2/3."
    }

