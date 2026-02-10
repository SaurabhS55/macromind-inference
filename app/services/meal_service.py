"""
Meal service - Core business logic for global read-through cache.
This is the money-maker logic.
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Food
from app.utils.normalize import normalize_food_name
from app.services.nutrition_service import fetch_nutrition


async def get_or_create_food(food_name: str, db: Session) -> Optional[Food]:
    """
    Get food from cache or create new entry (read-through cache pattern).
    
    Flow:
    1. Normalize food name
    2. Check MySQL cache
    3. If found → return instantly ⚡
    4. If not found → fetch from USDA API
    5. Store in cache
    6. Return
    
    Args:
        food_name: Raw food name from Vision API
        db: Database session
        
    Returns:
        Food object with nutrition data
        Returns None if food not found in USDA API
    """
    # Step 1: Normalize food name
    normalized = normalize_food_name(food_name)
    
    if not normalized:
        return None
    
    # Step 2: Check cache (MySQL lookup)
    food = db.query(Food).filter(
        Food.normalized_name == normalized
    ).first()
    
    # Step 3: Cache hit - return instantly
    if food:
        print(f"✅ CACHE HIT: {food_name} → {normalized}")
        return food
    
    # Step 4: Cache miss - fetch from USDA API
    print(f"❌ CACHE MISS: {food_name} → {normalized}")
    print(f"🔍 Fetching from USDA API...")
    
    nutrition = await fetch_nutrition(food_name)
    
    if not nutrition:
        print(f"⚠️  Not found in USDA: {food_name}")
        return None
    
    # Step 5: Store in cache
    new_food = Food(
        normalized_name=normalized,
        display_name=food_name,
        calories=nutrition["calories"],
        protein=nutrition["protein"],
        carbs=nutrition["carbs"],
        fats=nutrition["fats"]
    )
    
    db.add(new_food)
    db.commit()
    db.refresh(new_food)
    
    print(f"💾 CACHED: {food_name} → {normalized}")
    
    # Step 6: Return
    return new_food


def get_food_by_name(food_name: str, db: Session) -> Optional[Food]:
    """
    Get food from cache only (no API fallback).
    
    Args:
        food_name: Raw food name
        db: Database session
        
    Returns:
        Food object if found in cache, None otherwise
    """
    normalized = normalize_food_name(food_name)
    
    if not normalized:
        return None
    
    return db.query(Food).filter(
        Food.normalized_name == normalized
    ).first()
