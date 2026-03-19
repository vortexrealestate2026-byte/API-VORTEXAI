import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings

logger = logging.getLogger("vortex")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create all database tables."""
    from app.database import engine
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified on startup.")
    yield


app = FastAPI(
    title="VortexAI API",
    description="Two-sided SaaS platform: Real Estate Wholesale + Car Dealer Lead Generation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
allowed_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Log unhandled exceptions to DB and return a clean 500."""
    logger.error(f"Unhandled exception on {request.method} {request.url}: {exc}", exc_info=True)
    try:
        from app.database import SessionLocal
        from app.core.logging import log_event
        db = SessionLocal()
        try:
            log_event(
                db,
                level="error",
                service="api",
                message=f"Unhandled exception: {type(exc).__name__}: {exc}",
                details={"path": str(request.url), "method": request.method},
            )
        finally:
            db.close()
    except Exception:
        pass
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Health check
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


# Routers
from app.routes.auth import router as auth_router
from app.routes.leads import router as leads_router
from app.routes.buyers import router as buyers_router
from app.routes.dealers import router as dealers_router
from app.routes.car_leads import router as car_leads_router
from app.routes.webhooks import router as webhooks_router
from app.routes.dashboard import router as dashboard_router
from app.routes.logs import router as logs_router

app.include_router(auth_router)
app.include_router(leads_router)
app.include_router(buyers_router)
app.include_router(dealers_router)
app.include_router(car_leads_router)
app.include_router(webhooks_router)
app.include_router(dashboard_router)
app.include_router(logs_router)
