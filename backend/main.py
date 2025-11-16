from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.image_routes import router as image_router

app = FastAPI()

# Enable CORS so the frontend can communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Allow all frontend origins (hackathon-safe)
    allow_credentials=True,
    allow_methods=["*"],          # Allow all request methods (GET, POST, etc.)
    allow_headers=["*"],          # Allow all headers
)

# Register image-related endpoints
app.include_router(image_router)

# Basic health check endpoint
@app.get("/")
def root():
    return {"message": "Food Glasses API running"}

