"""Minimal project settings helpers."""

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    project_name: str
    app_env: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            project_name=os.getenv("PROJECT_NAME", "market_intelligence_platform"),
            app_env=os.getenv("APP_ENV", "local"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

