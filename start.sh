#!/bin/sh
python seed_owner.py
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
