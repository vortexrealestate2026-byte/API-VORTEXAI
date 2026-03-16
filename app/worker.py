
from fastapi import FastAPI
from .routes import deals, buyers, finance, auth

app = FastAPI(title="Rocket Autonomous API")

app.include_router(auth.router)
app.include_router(deals.router)
app.include_router(buyers.router)
app.include_router(finance.router)

@app.get("/health")
def health():
    return {"status":"running"}
