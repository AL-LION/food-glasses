import cv2
import numpy as np

def detect_dark_patches(img):
    """
    Detect significantly dark regions (possible bruising) on produce.
    Returns a list of issue tags (empty if none).
    """

    # Defensive: ensure image is RGB
    if img is None or img.size == 0:
        return []

    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Smooth noise
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        # Adaptive threshold to find darker-than-average regions
        # 255 = white (not dark), 0 = dark region
        thresh = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            35,   # window size
            10    # bias
        )

        # Find contours of dark blobs
        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        dark_area = 0
        total_area = img.shape[0] * img.shape[1]

        for c in contours:
            area = cv2.contourArea(c)
            if area > 100:     # ignore tiny noise specks
                dark_area += area

        # Ratio of dark-area to entire image
        ratio = dark_area / total_area

        # Heuristic threshold: bruising visible if > ~2.5%
        if ratio > 0.025:
            return ["Possible bruising (dark patches detected)"]

        return []

    except Exception:
        # If the heuristic fails, fail silently (don't break API)
        return []
