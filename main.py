from fastapi import FastAPI
from api.auth import router as auth_router

app = FastAPI(
    title="Article 11 API",
    description="API pour le projet Article 11",
    version="1.0.0",
    docs_url="/docs/",
)


app.include_router(auth_router)
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur Article 11 !"}