#!/bin/bash
# Azure App Service startup script for HR Portal
# Optimized for Azure Oryx Python runtime

echo "=== HR Portal Azure Startup ==="

# Azure App Service sets WEBSITE_HOSTNAME and other env vars
echo "Environment: ${APP_ENV:-production}"
echo "Website: ${WEBSITE_HOSTNAME:-unknown}"

# Navigate to the app directory
cd /home/site/wwwroot || exit 1

# Azure Oryx pre-builds dependencies during deployment
# We just need to start the application

# Get the port from Azure's PORT environment variable (defaults to 8000)
export PORT="${PORT:-8000}"
echo "Binding to port: $PORT"

# Use Gunicorn with Uvicorn workers (Azure best practice for FastAPI)
# - Gunicorn manages worker processes and restart
# - Uvicorn provides ASGI support for FastAPI
# - Bind to 0.0.0.0:$PORT so Azure can reach it
# - 1 worker for B1 tier, increase for higher tiers
# - Timeout increased to handle startup migrations

echo "Starting Gunicorn with Uvicorn workers..."
exec gunicorn app.main:app \
    --bind 0.0.0.0:$PORT \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
