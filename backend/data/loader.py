import json
from pathlib import Path

SHARED_PATH = Path(__file__).resolve().parents[2] / "shared" / "foods.json"

with open(SHARED_PATH, "r") as f:
    FOODS = json.load(f)
