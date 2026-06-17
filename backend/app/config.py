from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://mcu:mcu@db:3306/mcu_tracker"
    ENV: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        """Ensure the URL always uses the pymysql driver."""
        if v.startswith("mysql://"):
            return v.replace("mysql://", "mysql+pymysql://", 1)
        return v


settings = Settings()