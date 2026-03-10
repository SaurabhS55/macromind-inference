# 🍎 Nutrition Analysis API

## 🌟 Features

- **Smart Food Detection**: Gemini 2.5 Flash model for food and quantity detection
- **Accurate Nutrition Data**: USDA FoodData Central (government dataset)
- **Global Cache Pattern**: Read-through cache for instant lookups
- **Intelligent Normalization**: Maximizes cache hits, prevents duplicates

## 🏗️ Architecture

```
User uploads meal image
        ↓
Gemini 2.5 Flash Vision
        ↓
Detect foods + quantity
        ↓
Normalize food name
        ↓
Check Global Nutrition Lookup (MySQL)
        ↓
Found? → Return instantly ⚡
        ↓
Not found?
        ↓
Call USDA API
        ↓
Normalize + Store
        ↓
Return
```

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+ (running locally)
- USDA FoodData Central API key
- `transformers`, `torch`, and `Pillow` libraries (installed via requirements.txt)

## 🚀 Quick Start

### 1. Get API Key

**USDA FoodData Central API:**
1. Sign up at [USDA API Portal](https://fdc.nal.usda.gov/api-key-signup.html)
2. Get your free API key

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Update these values in `.env`:
```bash
USDA_API_KEY=your_usda_api_key_here
DB_PASSWORD=your_mysql_password
```

### 3. Start the API

```bash
# Make startup script executable
chmod +x start.sh

# Run the application
./start.sh
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### `POST /analyze`

Analyze meal image and return nutrition data.

**Request:**
```bash
curl -X POST \
  -F "file=@meal.jpg" \
  http://localhost:8000/analyze
```

{
  "success": true,
  "detected_foods": [{
        "name": "Apple",
        "quantity": "1 medium"
  },
  {
        "name": "Banana",
        "quantity": "1 medium"
  },
  {
        "name": "Orange",
        "quantity": "1 medium"
  }],
  "nutrition_data": [
    {
      "id": 1,
      "name": "Apple",
      "normalized_name": "apple",
      "nutrition": {
        "calories": 52.0,
        "protein": 0.26,
        "carbs": 13.81,
        "fats": 0.17
      },
      "cached_at": "2026-02-10T23:00:00"
    }
  ],
  "cache_hits": 2,
  "cache_misses": 1,
  "message": "Successfully analyzed 3 food items"
}
```

### `GET /health`

Health check with service status.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "food_model": "nateraw/food (HuggingFace)",
  "usda_api": "configured"
}
```

## 🗄️ Database Schema

```sql
CREATE TABLE foods (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    normalized_name VARCHAR(255) UNIQUE,
    display_name VARCHAR(255),
    calories FLOAT,
    protein FLOAT,
    carbs FLOAT,
    fats FLOAT,
    created_at TIMESTAMP,
    INDEX(normalized_name)
);
```

**Note:** All nutrition values are per 100g (industry standard).

## 🔧 Project Structure

```
macromind-ai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # MySQL connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services/
│   │   ├── vision_service.py    # HuggingFace Food Model
│   │   ├── nutrition_service.py # USDA API
│   │   └── meal_service.py      # Core cache logic
│   └── utils/
│       └── normalize.py     # Name normalization
├── init_db.sql              # Database schema
├── requirements.txt         # Python dependencies
├── start.sh                 # Startup script
├── .env.example             # Environment template
└── README.md
```

## 🧪 Testing

### Test with sample image:

```bash
# Download a test image
wget https://images.unsplash.com/photo-1546069901-ba9599a7e63c -O apple.jpg

# Analyze it
curl -X POST -F "file=@apple.jpg" http://localhost:8000/analyze
```

### Verify cache:

```bash
# First request - cache miss (fetches from USDA)
curl -X POST -F "file=@apple.jpg" http://localhost:8000/analyze

# Second request - cache hit (instant response)
curl -X POST -F "file=@apple.jpg" http://localhost:8000/analyze
```

### Check database:

```bash
mysql -u root -p nutrition_lookup -e "SELECT * FROM foods;"
```

## 🎯 Key Design Decisions

### 1. Normalization Strategy
All food names are normalized before database lookups:
- Lowercase conversion
- Remove special characters
- Normalize whitespace

This maximizes cache hits and prevents duplicate entries.

### 2. Per 100g Storage
Nutrition data is stored per 100g (not per serving) because serving sizes vary wildly across foods and regions.

### 3. Read-Through Cache
The cache pattern automatically fetches and stores missing data, eliminating manual cache management.

## 🐛 Troubleshooting

**MySQL Connection Failed:**
```bash
# Check MySQL is running
sudo systemctl status mysql

# Start MySQL
sudo systemctl start mysql
```

**Model Loading Issues:**
```bash
# Check if transformers is installed
pip show transformers

# The model downloads on first run (~300MB)
# Ensure you have internet connection for the first startup
```

**USDA API Error:**
```bash
# Verify API key
echo $USDA_API_KEY

# Test API key
curl "https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&api_key=$USDA_API_KEY"
```

## 📊 Performance

- **Cache Hit**: ~5ms (MySQL lookup)
- **Cache Miss**: ~1000ms (USDA API + MySQL insert)
- **Food Detection**: ~1-3s (Local AI processing)

After initial population, most requests are cache hits (instant response).

## 🔐 Security Notes

- Never commit `.env` or `*.json` credential files
- Use environment variables for all secrets
- Configure CORS appropriately for production
- Consider rate limiting for public APIs

## 📝 License

MIT License - Feel free to use in your projects!

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

<div align="center">

### 🚀 Built with passion by Saurabh Salunke

⭐ **Nutrition meets Intelligence** ⭐

**Cheers!** 🙃

</div>
