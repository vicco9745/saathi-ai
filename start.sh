#!/bin/sh
cd /app || exit 1
export PYTHONPATH=/app
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
