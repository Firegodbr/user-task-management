from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./app/db/test.db"
    DEBUG: bool = False

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }

# Create a settings instance
settings = Settings()
