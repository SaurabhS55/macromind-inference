"""
Example script to test the nutrition analysis API.
"""
import requests
import sys

API_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_analyze(image_path):
    """Test analyze endpoint with an image."""
    print(f"📸 Analyzing image: {image_path}")
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{API_URL}/analyze", files=files)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success!")
        print(f"Detected foods: {data['detected_foods']}")
        print(f"Cache hits: {data['cache_hits']}")
        print(f"Cache misses: {data['cache_misses']}")
        print(f"\nNutrition data:")
        
        for food in data['nutrition_data']:
            print(f"\n  🍎 {food['name']}")
            print(f"     Calories: {food['nutrition']['calories']} kcal")
            print(f"     Protein: {food['nutrition']['protein']} g")
            print(f"     Carbs: {food['nutrition']['carbs']} g")
            print(f"     Fats: {food['nutrition']['fats']} g")
    else:
        print(f"\n❌ Error: {response.text}")


if __name__ == "__main__":
    # Test health
    test_health()
    
    # Test analyze if image path provided
    if len(sys.argv) > 1:
        test_analyze(sys.argv[1])
    else:
        print("Usage: python test_api.py <image_path>")
        print("Example: python test_api.py apple.jpg")
