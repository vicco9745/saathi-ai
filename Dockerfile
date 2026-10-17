# Official Playwright Image (Isme Chrome pehle se hota hai)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Playwright ko batayein ki browser kahan milega (Image ka default path)
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 10000
CMD ["sh", "start.sh"]
