from fastapi import FastAPI
from app.api.routes.deals import router as deals_router

app = FastAPI(
    title="Vortex AI API",
    description="Backend API for the Vortex AI Deal Engine",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Vortex AI API Running"
    }

# Register routes
app.include_router(deals_router)
