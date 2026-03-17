# Vortex AI API

Backend API powering the **Vortex AI Deal Engine**.
This service manages real estate and vehicle deal pipelines, AI automation, and financing submissions.

---

# Core Features

• Wholesale real estate deal ingestion
• Vehicle inventory data pipelines
• Buyer matching engine
• Financing application submissions
• AI automation pipelines
• Background job processing with Celery

---

# Tech Stack

* **Python**
* **FastAPI**
* **Redis**
* **Celery**
* **Docker**
* **PostgreSQL**

---

# Project Architecture

```
app
│
├── api
│   └── routes
│
├── models
│
├── services
│
├── database
│   └── database.py
│
└── main.py
```

---

# Local Development

### 1. Clone the repository

```
git clone https://github.com/your-repo/vortex-ai-api.git
cd vortex-ai-api
```

### 2. Start the system with Docker

```
docker-compose up --build
```

---

# API Server

The API will run at:

```
http://localhost:8080
```

---

# API Documentation

Interactive API docs:

```
http://localhost:8080/docs
```

Swagger UI allows you to test all endpoints.

---

# Background Workers

Vortex AI uses **Celery + Redis** to process background tasks like:

* Property scraping
* Vehicle ingestion
* Deal scoring
* Buyer matching
* AI automation pipelines

Workers start automatically with Docker.

---

# Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@db:5432/vortex
REDIS_URL=redis://redis:6379
DATAFINITI_TOKEN=your_token_here
```

---

# Deployment

This backend is designed to deploy on:

* Railway
* Docker infrastructure
* Kubernetes environments

Production API example:

```
https://api-vortexai-production.up.railway.app
```

---

# License

Internal use for the **Vortex AI platform**.
