from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app/db/sqlite.db"
    DEBUG: bool = False
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ENV: str = "test"
    COOKIE_SECURE: bool = True  # Set to False for local development without HTTPS
    COOKIE_SAMESITE: str = "lax"  # "strict", "lax", or "none"
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Create a settings instance
settings = Settings()
