#!/bin/sh
cd /app/app || exit 1
export PYTHONPATH=/app
exec python -m uvicorn main:app --host 0.0.0.0 --port $PORT
