import cv2
import numpy as np

def detect_mold(img):
    """
    Detect green or white mold-like clusters using HSV masking.
    Returns a list of issue tags (empty if none detected).
    """

    if img is None or img.size == 0:
        return []

    try:
        # Convert to HSV (better for color segmentation)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # ----------------------------------------
        # GREEN MOLD RANGE
        # ----------------------------------------
        green_lower = np.array([35, 40, 40])    # light green
        green_upper = np.array([85, 255, 255])  # strong green
        green_mask = cv2.inRange(hsv, green_lower, green_upper)

        # ----------------------------------------
        # WHITE FUZZY MOLD RANGE
        # ----------------------------------------
        # Whites have low saturation and high value
        white_lower = np.array([0, 0, 180])
        white_upper = np.array([180, 80, 255])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)

        # Combine mold-like masks
        combined_mask = cv2.bitwise_or(green_mask, white_mask)

        # Clean up small noise
        kernel = np.ones((5, 5), np.uint8)
        cleaned = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)

        # Count how many pixels are mold-colored
        mold_pixels = np.count_nonzero(cleaned)
        total_pixels = img.shape[0] * img.shape[1]
        ratio = mold_pixels / total_pixels

        # Heuristic threshold: obvious mold if >= 1.5% of pixels
        if ratio > 0.015:
            return ["Possible mold (green/white clusters detected)"]

        return []

    except Exception:
        return []
