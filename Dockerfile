FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: run the API
# Override via Railway service start command:
#   Worker:    celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4
#   Beat:      celery -A app.tasks.celery_app beat --loglevel=info
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
