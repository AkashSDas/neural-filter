from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

# =========================================
# Environment Variables
# =========================================


class Settings(BaseSettings):
    app_name: str
    frontend_url: str
    db_url: str
    jwt_secret_key: str
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiry_in_min: int = Field(default=30)
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_tls: bool
    mail_ssl: bool
    use_credentials: bool
    backend_url: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore
