from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router
from api.users import router as users_router
from api.feed import router as feed_router
from api.demo import router as demo_router
from api.compromise import router as compromise_router
from middlewares.security import SecurityMiddleware
from db.init_db import initialize_database


app = FastAPI(
    title="Team 1 - Article 11 ",
    description="API for Article 11",
    version="1.0.2",
    docs_url="/docs/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hackaton-europe-2025-frontend.vercel.app/","https://hackaton-europe-2025-frontend-7tvd.vercel.app/", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(SecurityMiddleware)
app.include_router(auth_router, prefix="/auth")
app.include_router(feed_router)
app.include_router(users_router)
app.include_router(demo_router)
app.include_router(compromise_router)
@app.on_event("startup")
async def startup_event():
    initialize_database()

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur Article 11 !"}