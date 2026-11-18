import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
EVENTS_PATH = DATA_DIR / "security_events.json"
DATABASE_PATH = DATA_DIR / "sentinelai.sqlite3"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    APP_NAME: str = 'SentinelAI'
    APP_ENV: str = 'development'
    LOG_LEVEL: str = 'INFO'
    GOOGLE_API_KEY: SecretStr | None = None
    GEMINI_MODEL: str = 'gemini-3.5-flash'
    LANGSMITH_TRACING: bool = False
    LANGSMITH_API_KEY: SecretStr | None = None
    LANGSMITH_PROJECT: str = 'sentinelai'
    TAVILY_API_KEY: SecretStr | None = None
    TAVILY_MCP_URL: str = 'https://mcp.tavily.com/mcp/'
    sqlite_path: Path = Field(default=DATABASE_PATH)
    security_events_path: Path = Field(default=EVENTS_PATH)

    @property
    def database_path(self) -> Path:
        return self._absolute(self.sqlite_path)

    @property
    def events_path(self) -> Path:
        return self._absolute(self.security_events_path)

    @staticmethod
    def _absolute(path: Path) -> Path:
        return path if path.is_absolute() else PROJECT_ROOT / path


@lru_cache
def get_settings() -> Settings:
    return Settings()


def configure_model_environment() -> None:
    """Bridge settings into SDKs that only read process environment variables."""
    settings = get_settings()
    if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.get_secret_value():
        os.environ.setdefault('GOOGLE_API_KEY', settings.GOOGLE_API_KEY.get_secret_value())
    os.environ.setdefault('LANGSMITH_TRACING', str(settings.LANGSMITH_TRACING).lower())
    os.environ.setdefault('LANGSMITH_PROJECT', settings.LANGSMITH_PROJECT)
    if settings.LANGSMITH_API_KEY and settings.LANGSMITH_API_KEY.get_secret_value():
        os.environ.setdefault('LANGSMITH_API_KEY', settings.LANGSMITH_API_KEY.get_secret_value())
