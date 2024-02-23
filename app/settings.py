# settings.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Application"
    ADMIN_EMAIL: str
    items_per_user: int = 10

    class Config:
        env_file = "env/local.env"


settings = Settings()
