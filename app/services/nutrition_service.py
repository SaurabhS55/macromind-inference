"""
USDA FoodData Central API service for nutrition data.
"""
import os
import httpx
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()

# USDA API configuration
USDA_API_KEY = os.getenv("USDA_API_KEY")
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Nutrient IDs from USDA database
NUTRIENT_IDS = {
    "calories": 1008,  # Energy (kcal)
    "protein": 1003,   # Protein (g)
    "carbs": 1005,     # Carbohydrate (g)
    "fats": 1004,      # Total lipid (fat) (g)
}


async def fetch_nutrition(food_name: str) -> Optional[Dict[str, float]]:
    """
    Fetch nutrition data from USDA FoodData Central API.
    
    Args:
        food_name: Name of the food item to search
        
    Returns:
        Dictionary with calories, protein, carbs, fats per 100g
        Returns None if food not found
        
    Raises:
        Exception: If API call fails
    """
    if not USDA_API_KEY:
        raise Exception("USDA_API_KEY not configured in environment")
    
    try:
        params = {
            "query": food_name,
            "api_key": USDA_API_KEY,
            "pageSize": 1,  # Only need the top result
            "dataType": ["Survey (FNDDS)", "Foundation", "SR Legacy"]  # Prioritize quality data
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(USDA_BASE_URL, params=params)
            response.raise_for_status()
        
        data = response.json()
        
        # Check if any foods were found
        if not data.get("foods"):
            return None
        
        # Extract nutrients from first result
        food = data["foods"][0]
        nutrients = food.get("foodNutrients", [])
        
        # Helper function to extract nutrient value by ID
        def get_nutrient_value(nutrient_id: int) -> float:
            for nutrient in nutrients:
                if nutrient.get("nutrientId") == nutrient_id:
                    return nutrient.get("value", 0.0)
            return 0.0
        
        # Build nutrition dictionary
        nutrition = {
            "calories": get_nutrient_value(NUTRIENT_IDS["calories"]),
            "protein": get_nutrient_value(NUTRIENT_IDS["protein"]),
            "carbs": get_nutrient_value(NUTRIENT_IDS["carbs"]),
            "fats": get_nutrient_value(NUTRIENT_IDS["fats"]),
        }
        
        return nutrition
        
    except httpx.HTTPStatusError as e:
        raise Exception(f"USDA API HTTP error: {e.response.status_code}")
    except httpx.RequestError as e:
        raise Exception(f"USDA API request failed: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to fetch nutrition data: {str(e)}")
