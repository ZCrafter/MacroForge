from pydantic_settings import BaseSettings
from pydantic import field_validator
import os

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://macroforge:macroforge@db:5432/macroforge"
    jwt_secret_key: str = "change-me"
    admin_username: str = "admin"
    admin_password: str = "change-me"
    usda_api_key: str | None = None

    @field_validator("admin_password")
    @classmethod
    def debug_password(cls, v):
        print("DEBUG ENV PASSWORD (length):", len(v))
        return v

    class Config:
        env_file = ".env"

# Export an instance
settings = Settings()
