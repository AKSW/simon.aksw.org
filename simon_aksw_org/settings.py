"""Application Settings"""

import json
from datetime import UTC, datetime
from functools import lru_cache
from importlib.metadata import version
from logging import Logger, getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.templating import Jinja2Templates


class Settings(BaseSettings):
    """Application settings."""

    title: str = Field(default="Kondolenzbuch für unseren Kollegen Simon Bin")
    birth_date: str = Field(default="11.04.1986")
    death_date: str = Field(default="08.03.2026")
    version: str = Field(default=version("simon_aksw_org"))
    data_dir: Path = Field(
        default=Path(TemporaryDirectory(prefix="simon-aksw-org-").name),
        description="Data directory, where the JSON files are saved.",
    )
    static_dir: Path = Field(
        default=Path(__file__).parent / "static",
        description="Static folder. Where images and icons are loaded from.",
    )
    templates_dir: Path = Field(
        default=Path(__file__).parent / "templates",
        description="Template folder. Where the jinja2 html files are loaded from.",
    )
    published_date: str = Field(
        default=datetime.fromtimestamp(Path(__file__).stat().st_mtime, tz=UTC)
        .isoformat()
        .split("T")[0]
    )
    logger: Logger = Field(default=getLogger("uvicorn.error"), exclude=True)
    templates: Jinja2Templates = Field(
        default=Jinja2Templates(directory=TemporaryDirectory().name), exclude=True
    )
    allow_messages: bool = Field(default=True, description="Allow new submissions.")
    show_messages: bool = Field(default=True, description="Show submissions.")
    recaptcha_secret_key: SecretStr = Field(description="Recaptcha secret key.")
    recaptcha_site_key: str = Field(description="Recaptcha site key.")

    model_config = SettingsConfigDict(
        env_prefix="SIMON_AKSW_ORG_",
        extra="ignore",  # ignore extra envs such as TESTING_*
        validate_assignment=True,  # allow to change the settings object with re-validation
    )

    def model_post_init(self, context: Any) -> None:  # noqa: ARG002, ANN401
        """Post init"""
        self.data_dir = Path(self.data_dir).resolve()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.templates = Jinja2Templates(directory=self.templates_dir)
        self.logger.info("Application settings loaded")
        dictionary: dict = json.loads(self.model_dump_json())
        for key, value in dictionary.items():
            self.logger.info(f"Setting {key}: {value}")


@lru_cache
def get_settings() -> Settings:
    """Get Application settings (cached)"""
    return Settings()  # type:ignore[call-arg]
