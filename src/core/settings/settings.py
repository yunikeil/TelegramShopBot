from pathlib import Path

from pydantic import field_validator, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path, override=True)


class __Settings(BaseSettings):
    DEBUG: bool
    ECHO_SQL: bool
    RELOAD: bool
    TG_SHOP_TOKEN: str
    TG_LOG_TOKEN: str
    TG_LOG_CHANNEL: int
    
    BOT_VERSION: str
    ADMIN_NICKNAME: str
    MODER_IDS: list[int]
    
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_CONNECTION_APP_NAME: str

    DATABASE_USERNAME: str
    DATABASE_PASSWORD: SecretStr
    
    _PGADMIN_DEFAULT_EMAIL: str
    _PGADMIN_DEFAULT_PASSWORD: SecretStr
    
    MINIO_HOST: str
    MINIO_PORT: int
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: SecretStr
    MINIO_DEFAULT_BUCKETS: str
    
    @field_validator('BOT_VERSION', mode="before")
    @classmethod
    def bot_version_validator(cls, v: str):
        if v.count('.') != 2 or not all(part.isdigit() for part in v.split('.')):
            raise ValueError("BOT_VERSION must be a string with format 'x.y.z'")
        return v
    
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD.get_secret_value(),
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )
    
    @property
    def MINIO_URL(self) -> str:
        return self.MINIO_HOST + f":{self.MINIO_PORT}"

    model_config = SettingsConfigDict(
        env_file=env_path, env_file_encoding='utf-8', extra="allow")


config = __Settings()
