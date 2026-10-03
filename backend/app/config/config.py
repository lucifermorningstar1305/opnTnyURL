# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright (c) 2026 Adityam Ghosh
# SPDX-License-Identifier: MIT
#

import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    MACHINE_ID: str

    CORS_ORIGIN: str = pydantic.Field(default="*")
    CORS_ALLOWED_METHODS: str = pydantic.Field(default="*")

    VALKEY_HOST: str
    VALKEY_PORT: int = pydantic.Field(default=6379)
    VALKEY_DB: int = pydantic.Field(default=0)
    VALKEY_PASSWORD: str

    VALKEY_BLOOM_FILTER_NAME: str = pydantic.Field(default="opn_tny_url_bloom")
    VALKEY_BLOOM_FILTER_CAPACITY: int = pydantic.Field(default=1_000_000)
    VALKEY_BLOOM_FILTER_FP_RATE: float = pydantic.Field(default=1e-10)

    ASYNC_POSTGRES_URL: str
    POSTGRES_URL: str

    LOG_LEVEL: str = pydantic.Field(default="info")


Settings = Config()  # pyright: ignore
