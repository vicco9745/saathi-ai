# Saathi AI - Ultimate PDF Engine (Playwright + Chromium)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Browser install path set karo
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/render/project/.cache/playwright

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# System dependencies ke saath Chromium install karo
RUN playwright install --with-deps chromium

COPY . .
EXPOSE 10000
CMD ["sh", "start.sh"]
