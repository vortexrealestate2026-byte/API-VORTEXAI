from fastapi import FastAPI
from app.api.routes import deals
from app.api.routes import ai

app = FastAPI()

app.include_router(deals.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "Vortex AI running"}
