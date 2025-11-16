from fastapi import APIRouter
from backend.data.loader import FOODS

router = APIRouter()

@router.get("/food/{name}")
def get_food(name: str):
    name = name.lower()
    for item in FOODS:
        if item["name"] == name:
            return item
    return {"error": "Food not found"}

@router.get("/search")
def search_food(q: str):
    q = q.lower()
    matches = [item for item in FOODS if q in item["name"]]
    return {"results": matches}
