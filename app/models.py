"""
Database models for nutrition cache.
"""
from sqlalchemy import Column, BigInteger, String, Float, TIMESTAMP, Index
from sqlalchemy.sql import func
from app.database import Base


class Food(Base):
    """
    Global nutrition lookup table.
    Stores normalized food names with nutrition data per 100g.
    """
    __tablename__ = "foods"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    # Food identification
    normalized_name = Column(String(255), unique=True, nullable=False, index=True)
    display_name = Column(String(255), nullable=False)
    
    # Nutrition data (per 100g - industry standard)
    calories = Column(Float, nullable=False, default=0.0)
    protein = Column(Float, nullable=False, default=0.0)
    carbs = Column(Float, nullable=False, default=0.0)
    fats = Column(Float, nullable=False, default=0.0)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    def __repr__(self):
        return f"<Food(name='{self.display_name}', calories={self.calories})>"

    def to_dict(self):
        """Convert model to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.display_name,
            "normalized_name": self.normalized_name,
            "nutrition": {
                "calories": self.calories,
                "protein": self.protein,
                "carbs": self.carbs,
                "fats": self.fats
            },
            "cached_at": self.created_at.isoformat() if self.created_at else None
        }
