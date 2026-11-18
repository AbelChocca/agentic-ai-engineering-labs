import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    app_name: str = 'SentinelAI'
    app_env: str = 'development'
    log_level: str = 'INFO'
    google_api_key: SecretStr | None = None
    gemini_model: str = 'gemini-3.5-flash'
    langsmith_tracing: bool = False
    langsmith_api_key: SecretStr | None = None
    langsmith_project: str = 'sentinelai'
    tavily_api_key: SecretStr | None = None
    tavily_mcp_url: str = 'https://mcp.tavily.com/mcp/'
    sqlite_path: Path = Field(default=Path('data/sentinelai.sqlite3'))
    security_events_path: Path = Field(default=Path('data/security_events.json'))

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
    if settings.google_api_key and settings.google_api_key.get_secret_value():
        os.environ.setdefault('GOOGLE_API_KEY', settings.google_api_key.get_secret_value())
    os.environ.setdefault('LANGSMITH_TRACING', str(settings.langsmith_tracing).lower())
    os.environ.setdefault('LANGSMITH_PROJECT', settings.langsmith_project)
    if settings.langsmith_api_key and settings.langsmith_api_key.get_secret_value():
        os.environ.setdefault('LANGSMITH_API_KEY', settings.langsmith_api_key.get_secret_value())
