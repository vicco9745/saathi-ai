FROM mcr.microsoft.com/playwright/python:v1.49.0-noble

WORKDIR /app

# Ye line Chrome ko sahi jagah dhundhne ke liye majboor karegi
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 10000
CMD ["sh", "start.sh"]
