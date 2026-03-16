from fastapi import FastAPI
from app.api.routes import deals

app = FastAPI()

app.include_router(deals.router)

@app.get("/")
def root():
    return {"message": "Vortex AI running"}
