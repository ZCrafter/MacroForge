from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://macroforge:macroforge@db:5432/macroforge"
    jwt_secret_key: str = "change-me"
    admin_username: str = "admin"
    admin_password: str = "change-me"
    usda_api_key: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
