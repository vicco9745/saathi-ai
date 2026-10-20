FROM mcr.microsoft.com/playwright/python:v1.49.0-noble
WORKDIR /app
ENV PYTHONPATH=/app
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium && \
    python -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print('Chromium executable:', p.chromium.executable_path); import os; assert os.path.isfile(p.chromium.executable_path), 'Chromium executable missing'; p.stop()" 
COPY . /app
EXPOSE 10000
CMD ["sh", "start.sh"]
