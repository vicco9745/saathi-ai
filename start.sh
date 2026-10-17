#!/bin/sh
cd /app || exit 1
python seed_owner.py
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
