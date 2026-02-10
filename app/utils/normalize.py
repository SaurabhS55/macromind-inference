"""
Food name normalization utility.
Critical for maximizing cache hits and preventing duplicate entries.
"""
import re


def normalize_food_name(name: str) -> str:
    """
    Normalize food name for consistent database lookups.
    
    Normalization steps:
    1. Convert to lowercase
    2. Remove all non-alphanumeric characters (except spaces)
    3. Normalize whitespace (collapse multiple spaces to one)
    4. Strip leading/trailing whitespace
    
    Args:
        name: Raw food name from Vision API or user input
        
    Returns:
        Normalized food name suitable for database lookup
        
    Examples:
        >>> normalize_food_name("Apple!")
        'apple'
        >>> normalize_food_name("Grilled  Chicken")
        'grilled chicken'
        >>> normalize_food_name("Pizza (Pepperoni)")
        'pizza pepperoni'
    """
    # Convert to lowercase
    name = name.lower().strip()
    
    # Remove all non-alphanumeric characters except spaces
    name = re.sub(r'[^a-z0-9\s]', '', name)
    
    # Normalize whitespace (collapse multiple spaces)
    name = re.sub(r'\s+', ' ', name)
    
    # Final strip
    name = name.strip()
    
    return name
