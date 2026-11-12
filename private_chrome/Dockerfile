FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn playwright==1.48.0
COPY app.py .
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}"]
