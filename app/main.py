from fastapi import FastAPI

app = FastAPI(title="Vortex AI Platform")


@app.get("/")
def root():
    return {"message": "Vortex AI Platform Running"}
