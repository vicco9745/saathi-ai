#!/bin/sh
# Force render to use port 10000
cd /app || exit 1
export PYTHONPATH=/app
python seed_owner.py
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 10000
