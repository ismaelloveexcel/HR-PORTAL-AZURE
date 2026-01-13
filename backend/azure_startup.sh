#!/bin/bash
# Azure App Service startup script for HR Portal
set -e

echo "=== HR Portal Azure Startup ==="

# Navigate to the app directory (files are in wwwroot, not wwwroot/backend)
cd /home/site/wwwroot

# Find Python - Azure App Service uses /opt/python or antenv
PYTHON_PATH=""
if [ -f "antenv/bin/python" ]; then
    PYTHON_PATH="antenv/bin/python"
    source antenv/bin/activate
elif [ -d "/opt/python" ]; then
    # Find the Python version installed
    PYTHON_VERSION=$(ls /opt/python/ | head -1)
    PYTHON_PATH="/opt/python/${PYTHON_VERSION}/bin/python3"
else
    PYTHON_PATH="python3"
fi

echo "Using Python: $PYTHON_PATH"

# Create virtual environment if it doesn't exist
if [ ! -d "antenv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_PATH -m venv antenv
    source antenv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations with Alembic
echo "Running database migrations..."
python -m alembic upgrade head || echo "Alembic migrations skipped (may need manual run)"

# Initialize database tables (create if not exist - fallback)
echo "Initializing database tables..."
python -c "
import asyncio
from app.database import engine
from app.models import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database tables created/verified successfully')

asyncio.run(init_db())
" || echo "Database init skipped (may already exist)"

# Start the application
echo "Starting uvicorn server on port 8000..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
