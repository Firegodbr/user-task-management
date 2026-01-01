from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app/db/test.db"
    DEBUG: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Create a settings instance
settings = Settings()
