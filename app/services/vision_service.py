"""
Gemini Vision service for MacroMind
Detects food items, quantity, and estimated nutrition from meal images.
"""

import json
import traceback
import os
from typing import Dict, Any

from google import genai
from google.genai import types
from dotenv import load_dotenv

from app.utils.prompt_loader import load_prompt


load_dotenv()

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load prompts
SYSTEM_PROMPT = load_prompt("system_prompt.txt")
USER_PROMPT = load_prompt("user_prompt.txt")


def detect_food(image_bytes: bytes) -> Dict[str, Any]:
    """
    Detect food items and estimate nutrition using Gemini Vision.

    Args:
        image_bytes: raw image bytes

    Returns:
        Dict containing detected foods and nutrition
    """

    try:

        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=SYSTEM_PROMPT),
                    types.Part.from_text(text=USER_PROMPT),
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/jpeg"
                    )
                ]
            )
        ],
        config={
            "response_mime_type": "application/json"
        }
    )

        # Extract text safely
        text = response.text.strip()

        # Remove markdown if model adds it
        text = text.replace("```json", "").replace("```", "").strip()

        # Parse JSON
        data = json.loads(text)

        return data

    except json.JSONDecodeError:
        print("🔴 Failed to parse Gemini JSON output")
        print("Raw response:", text)
        raise Exception("Invalid JSON returned from Gemini")

    except Exception as e:
        print(f"🔴 Gemini detect_food error: {type(e).__name__}: {repr(e)}")
        traceback.print_exc()
        raise Exception(f"Food detection failed: {str(e)}")