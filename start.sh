#!/bin/sh
cd /app || exit 1
export PYTHONPATH=/app
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
