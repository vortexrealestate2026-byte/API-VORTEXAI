from fastapi import FastAPI

from app.api.routes import deals
from app.api.routes import properties
from app.api.routes import pipeline

app = FastAPI(title="Vortex AI API")

app.include_router(deals.router)
app.include_router(properties.router)
app.include_router(pipeline.router)

@app.get("/")
def root():
    return {"message": "Vortex AI running"}
