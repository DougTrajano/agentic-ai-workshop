"""This module contains application settings using Pydantic."""

from typing import Literal

from pydantic import Field, computed_field, model_validator
from pydantic_settings import BaseSettings
from typing_extensions import Self


class Settings(BaseSettings):
    """Application settings."""

    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(
        default='INFO', description='Logging level'
    )

    ENABLE_HEADER_AUTH: bool = Field(
        default=False, description='Enable header-based authentication'
    )
    ENABLE_PASSWORD_AUTH: bool = Field(
        default=False, description='Enable password-based authentication'
    )

    DATABRICKS_HOST: str | None = Field(default=None, description='Databricks host URL')
    DATABRICKS_TOKEN: str | None = Field(
        default=None, description='Databricks personal access token'
    )

    # Lakebase
    # DATABASE_INSTANCE: str = Field(..., description='Database instance name')

    PGHOST: str | None = Field(default=None, description='PostgreSQL host')
    PGPORT: int = Field(default=5432, description='PostgreSQL port')
    PGUSER: str | None = Field(default=None, description='PostgreSQL user')
    PGDATABASE: str | None = Field(default=None, description='PostgreSQL database name')
    PGSSLMODE: str = Field(default='require', description='PostgreSQL SSL mode')

    @computed_field
    @property
    def pg_connection_string(self) -> str:
        """Construct the PostgreSQL connection string."""
        return (
            f'postgresql+psycopg://{self.PGUSER}:@{self.PGHOST}:'
            f'{self.PGPORT}/{self.PGDATABASE}?sslmode={self.PGSSLMODE}'
        )

    @model_validator(mode='after')
    def validate_auth_methods(self) -> Self:
        """Validate that only one authentication method is enabled."""
        if self.ENABLE_HEADER_AUTH and self.ENABLE_PASSWORD_AUTH:
            raise ValueError('Both header and password auth cannot be enabled simultaneously')
        if not self.ENABLE_HEADER_AUTH and not self.ENABLE_PASSWORD_AUTH:
            raise ValueError('At least one auth method must be enabled')
        return self


settings = Settings()
