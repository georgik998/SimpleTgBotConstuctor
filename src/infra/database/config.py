from pydantic_settings import BaseSettings
from pydantic import field_validator

from src.config import SETTINGS_CONFIG_DICT


class PostgresSettings(BaseSettings):
    model_config = SETTINGS_CONFIG_DICT

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_DSN: str | None = None

    @field_validator('POSTGRES_DSN')
    def build_db_url(cls, v, values):
        values = values.data
        if v is None:
            user = values['POSTGRES_USER']
            password = values['POSTGRES_PASSWORD']
            host = values['POSTGRES_HOST']
            port = values['POSTGRES_PORT']
            db = values['POSTGRES_DB']
            return (
                f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
            )
        return v


postgres_settings = PostgresSettings()
