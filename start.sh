#!/bin/sh
cd /app || exit 1
exec /usr/local/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT
