"""
FastAPI application - Global Read-Through Nutrition Cache API.
"""
import os
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, init_db
from app.services.vision_service import detect_food_sync
from app.services.meal_service import get_or_create_food
from app.schemas import AnalyzeResponse, ErrorResponse, FoodItem
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Nutrition Analysis API",
    description="Global read-through nutrition cache with Google Vision API and USDA FoodData Central",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    print("🚀 Starting Nutrition Analysis API...")
    print("📊 Initializing database...")
    init_db()
    print("✅ Database initialized")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Nutrition Analysis API",
        "version": "1.0.0"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_meal(
    file: UploadFile = File(..., description="Image file containing food"),
    db: Session = Depends(get_db)
):
    """
    Analyze meal image and return nutrition data.
    
    Flow:
    1. Upload meal image
    2. Google Vision API → detect food names
    3. For each food:
       - Normalize food name
       - Check Global Nutrition Lookup (MySQL)
       - Found? → Return instantly ⚡
       - Not found? → Call USDA API → Store → Return
    
    Args:
        file: Image file (JPEG, PNG, etc.)
        db: Database session
        
    Returns:
        AnalyzeResponse with detected foods and nutrition data
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image"
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        if len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )
        
        # Step 1: Detect foods using Vision API
        print(f"\n🔍 Analyzing image: {file.filename}")
        detected_labels = detect_food_sync(image_bytes)
        
        if not detected_labels:
            return AnalyzeResponse(
                success=True,
                detected_foods=[],
                nutrition_data=[],
                message="No food items detected in image"
            )
        
        print(f"👁️  Vision API detected: {detected_labels}")
        
        # Step 2: Get nutrition data for each detected food
        nutrition_data = []
        cache_hits = 0
        cache_misses = 0
        
        for food_name in detected_labels:
            # Check cache size before fetching
            initial_count = db.query(db.query(Food).count()).scalar() if 'Food' in dir() else 0
            
            food = await get_or_create_food(food_name, db)
            
            if food:
                nutrition_data.append(FoodItem(
                    id=food.id,
                    name=food.display_name,
                    normalized_name=food.normalized_name,
                    nutrition={
                        "calories": food.calories,
                        "protein": food.protein,
                        "carbs": food.carbs,
                        "fats": food.fats
                    },
                    cached_at=food.created_at.isoformat() if food.created_at else None
                ))
                
                # Check if it was a cache hit or miss
                final_count = db.query(db.query(Food).count()).scalar() if 'Food' in dir() else 0
                if final_count > initial_count:
                    cache_misses += 1
                else:
                    cache_hits += 1
        
        print(f"\n📊 Results: {len(nutrition_data)} foods analyzed")
        print(f"⚡ Cache hits: {cache_hits}")
        print(f"🔍 Cache misses: {cache_misses}\n")
        
        return AnalyzeResponse(
            success=True,
            detected_foods=detected_labels,
            nutrition_data=nutrition_data,
            cache_hits=cache_hits,
            cache_misses=cache_misses,
            message=f"Successfully analyzed {len(nutrition_data)} food items"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze image: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "vision_api": "configured" if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") else "not configured",
        "usda_api": "configured" if os.getenv("USDA_API_KEY") else "not configured"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )
