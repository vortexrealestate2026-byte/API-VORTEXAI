from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import deals
from app.api.routes import properties
from app.api.routes import vehicles
from app.api.routes import ai

app = FastAPI(title="Vortex AI")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(deals.router, prefix="/deals")
app.include_router(properties.router, prefix="/properties")
app.include_router(vehicles.router, prefix="/vehicles")
app.include_router(ai.router, prefix="/ai")

@app.get("/")
def root():
    return {"message": "Vortex AI running"}
