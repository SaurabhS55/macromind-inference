# 🍎 Nutrition Analysis API

**Global Read-Through Nutrition Cache** - A production-ready nutrition analysis API using Google Vision API, USDA FoodData Central API, and MySQL caching.

## 🌟 Features

- **Smart Food Detection**: Google Vision API with 80% confidence threshold
- **Accurate Nutrition Data**: USDA FoodData Central (government dataset)
- **Global Cache Pattern**: Read-through cache for instant lookups
- **Intelligent Normalization**: Maximizes cache hits, prevents duplicates
- **Production Ready**: Async, error handling, connection pooling

## 🏗️ Architecture

```
User uploads meal image
        ↓
Google Vision API → detects food names
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
- Google Cloud Vision API credentials
- USDA FoodData Central API key

## 🚀 Quick Start

### 1. Get API Keys

**Google Cloud Vision API:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Vision API
4. Create service account and download JSON key
5. Save as `google-vision-key.json`

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
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/google-vision-key.json
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

**Response:**
```json
{
  "success": true,
  "detected_foods": ["Apple", "Banana", "Orange"],
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
  "vision_api": "configured",
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
│   │   ├── vision_service.py    # Google Vision API
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

### 3. Confidence Threshold
Vision API labels are filtered at 80% confidence to reduce garbage entries in the database.

### 4. Read-Through Cache
The cache pattern automatically fetches and stores missing data, eliminating manual cache management.

## 🐛 Troubleshooting

**MySQL Connection Failed:**
```bash
# Check MySQL is running
sudo systemctl status mysql

# Start MySQL
sudo systemctl start mysql
```

**Vision API Error:**
```bash
# Verify credentials path
echo $GOOGLE_APPLICATION_CREDENTIALS

# Test credentials
gcloud auth application-default print-access-token
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
- **Cache Miss**: ~500ms (USDA API + MySQL insert)
- **Vision API**: ~1-2s (food detection)

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

### 🚀 Built with passion by Saurabh

*Powered by FastAPI • Google Vision API • USDA FoodData Central*

⭐ **Nutrition meets Intelligence** ⭐

**Cheers!** 🙃

</div>
