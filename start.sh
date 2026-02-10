#!/bin/bash

# Nutrition Analysis API Startup Script

echo "🚀 Starting Nutrition Analysis API..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Please copy .env.example to .env and configure your API keys"
    echo ""
    echo "cp .env.example .env"
    echo ""
    exit 1
fi

# Load environment variables
source .env

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check MySQL connection
echo "🔍 Checking MySQL connection..."
if ! mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1;" > /dev/null 2>&1; then
    echo "❌ MySQL connection failed!"
    echo "Please ensure MySQL is running and credentials in .env are correct"
    exit 1
fi

# Initialize database
echo "📊 Initializing database..."
mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASSWORD" < init_db.sql

# Check required API keys
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "⚠️  Warning: GOOGLE_APPLICATION_CREDENTIALS not set"
fi

if [ -z "$USDA_API_KEY" ]; then
    echo "⚠️  Warning: USDA_API_KEY not set"
fi

# Start the application
echo "✅ Starting FastAPI server..."
echo ""
python -m uvicorn app.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8000} --reload
