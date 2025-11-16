# Food Glasses
A lightweight web app that helps users check the freshness of produce using image analysis or quick item lookups.

Food Glasses lets users upload a photo of their fruits or vegetables to estimate freshness based on a small ONNX model and heuristic spoilage checks. Users can also search for an item to view shelf-life info, unsafe signs, and storage tips. The goal is to support more mindful food storage and reduce household food waste.

## Features
- Photo-based freshness check using ONNX Runtime
- Produce lookup with shelf-life, unsafe signs, and storage guidance
- Heuristic spoilage detection (dark patches, mold-like clusters, etc.)
- Clean React + Tailwind UI
- Modular backend pipeline using FastAPI

## How It Works
1. User uploads an image or searches for produce.
2. Backend identifies the item using an ONNX classification model.
3. Heuristic checks scan for visible spoilage cues.
4. Freshness data (lifespan, unsafe signs, storage tips) is pulled from a JSON file.
5. The frontend displays a combined “freshness verdict.”

## Tech Stack
Frontend: 
- React
- Vite
- Tailwind CSS

Backend:
- FastAPI
- Python
- ONNX Runtime
- JSON database
