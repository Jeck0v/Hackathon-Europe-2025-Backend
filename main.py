from fastapi import FastAPI
from api.auth import router as auth_router
from middlewares.security import SecurityMiddleware

app = FastAPI(
    title="Article 11 API",
    description="API pour le projet Article 11",
    version="1.0.0",
    docs_url="/docs/",
)

app.add_middleware(SecurityMiddleware)
app.include_router(auth_router, prefix="/auth")
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur Article 11 !"}