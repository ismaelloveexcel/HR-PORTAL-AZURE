#!/bin/bash
# Production startup script that uses PORT environment variable
PORT="${PORT:-5000}"
exec uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
