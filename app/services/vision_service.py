"""
Google Cloud Vision API service for food detection.
"""
import os
from typing import List
from google.cloud import vision
from dotenv import load_dotenv

load_dotenv()

# Initialize Vision API client
client = vision.ImageAnnotatorClient()

# Confidence threshold for label detection
CONFIDENCE_THRESHOLD = 0.80


async def detect_food(image_bytes: bytes) -> List[str]:
    """
    Detect food items in an image using Google Vision API.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        List of detected food labels with confidence > 80%
        
    Raises:
        Exception: If Vision API call fails
    """
    try:
        # Create Vision API image object
        image = vision.Image(content=image_bytes)
        
        # Perform label detection
        response = client.label_detection(image=image)
        
        # Check for errors
        if response.error.message:
            raise Exception(f"Vision API error: {response.error.message}")
        
        # Filter labels by confidence score
        labels = [
            label.description
            for label in response.label_annotations
            if label.score > CONFIDENCE_THRESHOLD
        ]
        
        return labels
        
    except Exception as e:
        raise Exception(f"Failed to detect food: {str(e)}")


def detect_food_sync(image_bytes: bytes) -> List[str]:
    """
    Synchronous version of detect_food for compatibility.
    
    Args:
        image_bytes: Raw image bytes
        
    Returns:
        List of detected food labels with confidence > 80%
    """
    try:
        image = vision.Image(content=image_bytes)
        response = client.label_detection(image=image)
        
        if response.error.message:
            raise Exception(f"Vision API error: {response.error.message}")
        
        labels = [
            label.description
            for label in response.label_annotations
            if label.score > CONFIDENCE_THRESHOLD
        ]
        
        return labels
        
    except Exception as e:
        raise Exception(f"Failed to detect food: {str(e)}")
