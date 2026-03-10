"""
Pydantic schemas for API request/response validation.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class NutritionData(BaseModel):
    """Nutrition information per 100g."""
    calories: float = Field(..., description="Calories (kcal)")
    protein: float = Field(..., description="Protein (g)")
    carbs: float = Field(..., description="Carbohydrates (g)")
    fats: float = Field(..., description="Fats (g)")


class DetectedFood(BaseModel):
    """Detected food item."""
    name: str
    quantity: str


class FoodItem(BaseModel):
    """Individual food item with nutrition data."""
    id: int
    name: str
    normalized_name: str
    nutrition: NutritionData
    cached_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnalyzeResponse(BaseModel):
    """Response from /analyze endpoint."""
    success: bool
    detected_foods: List[DetectedFood] = Field(default_factory=list, description="Foods detected by Vision API")
    nutrition_data: List[FoodItem] = Field(default_factory=list, description="Nutrition data for detected foods")
    cache_hits: int = Field(0, description="Number of foods found in cache")
    cache_misses: int = Field(0, description="Number of foods fetched from API")
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = False
    error: str
    detail: Optional[str] = None
