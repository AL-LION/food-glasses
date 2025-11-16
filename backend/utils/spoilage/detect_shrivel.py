import cv2
import numpy as np

def detect_shrivel(img):
    """
    Detect shriveling / wrinkling based on edge density.
    Higher edge density often indicates dried, wrinkled, or collapsed skin.
    Returns a list of issue tags (empty if none).
    """

    if img is None or img.size == 0:
        return []

    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Slight blur to remove noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Count edge pixels
        edge_pixels = np.count_nonzero(edges)
        total_pixels = img.shape[0] * img.shape[1]

        edge_ratio = edge_pixels / total_pixels

        # Heuristic threshold:
        # Fresh produce ~0.01–0.03
        # Wrinkled produce often ~0.05+
        if edge_ratio > 0.015:
            return ["Possible shriveling (wrinkled texture detected)"]

        return []

    except Exception:
        return []
