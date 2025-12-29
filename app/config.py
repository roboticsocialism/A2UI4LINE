from __future__ import annotations

import os

from dotenv import load_dotenv


def load_env() -> None:
    load_dotenv()


def env_str(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v


def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v.lower() in {"1", "true", "yes", "y"}


class Settings:
    def __init__(self) -> None:
        load_env()
        self.port = int(env_str("PORT", "3000") or "3000")
        self.env = env_str("ENV", "development") or "development"
        self.allow_insecure_dev = env_bool("ALLOW_INSECURE_DEV", default=False)

        self.line_channel_secret = env_str("LINE_CHANNEL_SECRET")
        self.line_channel_access_token = env_str("LINE_CHANNEL_ACCESS_TOKEN")


settings = Settings()
