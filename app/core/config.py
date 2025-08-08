from pydantic import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # count as 1 day
    DEBUG: bool = False
    class Config:
        env_file = ".env"
settings = Settings()
