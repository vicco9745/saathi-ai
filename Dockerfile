# Official Playwright Image (isme Chrome pehle se hota hai)
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Playwright ko batayein ki browser kahan milega
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Browser aur uski system libraries install karo
RUN playwright install --with-deps chromium

COPY . .
EXPOSE 10000
CMD ["sh", "start.sh"]
