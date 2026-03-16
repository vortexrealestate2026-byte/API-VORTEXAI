version: "3.9"

services:

  api:
    build: .
    container_name: vortex_api
    ports:
      - "8000:8000"
    depends_on:
      - redis
    volumes:
      - .:/app

  worker:
    build: .
    container_name: vortex_worker
    command: celery -A app.worker worker --loglevel=info
    depends_on:
      - redis
    volumes:
      - .:/app

  redis:
    image: redis:7
    container_name: vortex_redis
    ports:
      - "6379:6379"
