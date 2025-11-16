from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.image_routes import router as image_router
from backend.api.food_routes import router as food_router

app = FastAPI()   # <-- MUST come first

# Enable CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all frontend origins (hackathon-safe)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(image_router)
app.include_router(food_router)

# Health check
@app.get("/")
def root():
    return {"message": "Food Glasses API running"}


