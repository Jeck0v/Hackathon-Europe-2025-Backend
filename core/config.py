from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()