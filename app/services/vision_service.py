"""
HuggingFace food detection service using nateraw/food model (ViT fine-tuned on Food-101).
Runs locally — no API keys or billing required.
"""
import io
import traceback
from typing import List
from PIL import Image

# Lazy-initialized model pipeline
_pipeline = None

# Confidence threshold for classification
CONFIDENCE_THRESHOLD = 0.20

# Max number of top predictions to return
TOP_K = 5


def _get_pipeline():
    """Lazily initialize and return the HuggingFace image classification pipeline."""
    global _pipeline
    if _pipeline is None:
        print("🤖 Loading HuggingFace food detection model (nateraw/food)...")
        from transformers import pipeline
        _pipeline = pipeline("image-classification", model="nateraw/food")
        print("✅ Food detection model loaded")
    return _pipeline


def _format_label(label: str) -> str:
    """Convert model label to human-readable food name.
    
    The nateraw/food model returns labels like 'french_fries', 'hot_dog', etc.
    This converts them to 'French Fries', 'Hot Dog'.
    """
    return label.replace("_", " ").title()


async def detect_food(image_bytes: bytes) -> List[str]:
    """
    Detect food items in an image using HuggingFace food classification model.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        List of detected food labels above confidence threshold
        
    Raises:
        Exception: If classification fails
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        pipe = _get_pipeline()
        results = pipe(image, top_k=TOP_K)
        
        labels = [
            _format_label(r["label"])
            for r in results
            if r["score"] > CONFIDENCE_THRESHOLD
        ]
        
        return labels
        
    except Exception as e:
        print(f"🔴 detect_food error: {type(e).__name__}: {repr(e)}")
        traceback.print_exc()
        raise Exception(f"Failed to detect food: {type(e).__name__}: {str(e)}") from e


def detect_food_sync(image_bytes: bytes) -> List[str]:
    """
    Synchronous version of detect_food.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        List of detected food labels above confidence threshold
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        pipe = _get_pipeline()
        results = pipe(image, top_k=TOP_K)
        
        print(f"🔍 Raw model predictions: {results}")
        
        labels = [
            _format_label(r["label"])
            for r in results
            if r["score"] > CONFIDENCE_THRESHOLD
        ]
        
        return labels
        
    except Exception as e:
        print(f"🔴 detect_food_sync error: {type(e).__name__}: {repr(e)}")
        traceback.print_exc()
        raise Exception(f"Failed to detect food: {type(e).__name__}: {str(e)}") from e
