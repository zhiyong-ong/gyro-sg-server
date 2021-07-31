import os
import secrets
from pathlib import Path
from typing import Optional, Any, Dict

from pydantic import BaseSettings, PostgresDsn, validator

DEV = "dev"
PROD = "prod"

CUR_ENV = os.environ.get("GYROSG_API_ENV", DEV)


def parse_version_file(content: str):
    lines = [tuple(line.split("=")) for line in content.split("\n") if line]
    return {line[0]: line[1] for line in lines}


def get_version():
    file_path = Path(__file__).parent.parent.parent / "version.txt"
    with open(file_path, "r") as f:
        version = parse_version_file(f.read())
        return "{major}.{minor}.{patch}".format(**version)


def get_secret():
    file_path = Path(__file__).parent.parent.parent / "secrets.txt"
    with open(file_path, "r") as f:
        secret_content = f.read().strip()
    return secret_content


class Settings(BaseSettings):
    PROJECT_NAME = "Gyro SG"
    VERSION = get_version()
    SECRET_KEY: str = get_secret()
    API_V1_STR: str = "/api/v1"

    DB_USER: str = "gyrosg"
    DB_PASSWORD: str = "gyrosg"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "gyrosg"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, sqlalchemy_database_url: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(sqlalchemy_database_url, str):
            return sqlalchemy_database_url
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("DB_HOST"),
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_NAME', '')}",
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ProdConfig(Settings):
    DEVELOPMENT = False


class DevConfig(Settings):
    DEVELOPMENT = True


ENVIRONMENT_MAP = {
    DEV: DevConfig(),
    PROD: ProdConfig(),
}


def get_config(environment: str):
    return ENVIRONMENT_MAP[environment]


CONFIG = get_config(CUR_ENV)
