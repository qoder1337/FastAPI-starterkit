import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
APPDIR = os.path.abspath(os.path.dirname(__file__))


class EnvLoader(BaseSettings):
    APP_ENV: str = "development"  # Fallback

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASEDIR, ".env"),
        extra="ignore",  # Ignore everything else in .env
    )


class AppSettings(BaseSettings):
    APP_ENV: str
    APP_NAME: str
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"
    OPENAPI_URL: str | None = "/openapi.json"
    # EXT_DB: str
    # PRIVATE_API_KEY: str
    DEBUG: bool
    RELOAD: bool
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASEDIR, ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


class ProductionConfig(AppSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///" + os.path.join(
        APPDIR, "database", "db", "production.db"
    )
    DOCS_URL: None = None
    REDOC_URL: None = None
    OPENAPI_URL: None = None
    # EXT_DB: str = os.getenv("EXT_DB")
    DEBUG: bool = False
    RELOAD: bool = False
    APP_NAME: str = "Starter for FastAPI (Production)"


class DevelopmentConfig(AppSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///" + os.path.join(
        APPDIR, "database", "db", "development.db"
    )
    # EXT_DB: str = os.getenv("EXT_DB")
    DEBUG: bool = True
    RELOAD: bool = True
    APP_NAME: str = "Starter for FastAPI (Development)"


class TestingConfig(AppSettings):
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///" + os.path.join(
        APPDIR, "database", "db", "test.db"
    )
    # EXT_DB: str = os.getenv("EXT_DB")
    DEBUG: bool = True
    RELOAD: bool = True
    LOG_LEVEL: str = "WARNING"  # dont spam testresults
    APP_NAME: str = "Starter for FastAPI (Testing)"


config_setting = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

# choose_setting = os.getenv("APP_ENV", "development")

choose_setting = EnvLoader().APP_ENV
SET_CONF = config_setting[choose_setting]()


if __name__ == "__main__":
    print(f"{BASEDIR=}")
    print(f"{APPDIR=}")
    print(SET_CONF)
