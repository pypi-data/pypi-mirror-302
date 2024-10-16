import os
from typing import Dict, Type

from pydantic_settings import BaseSettings

from simba_sdk.core.requests.middleware.manager import BaseMiddleware
from simba_sdk.core.requests.middleware.trailing_slash import (
    UrlAppendTrailingSlashHandler,
)


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    middleware: Dict[str, Type[BaseMiddleware]] = {
        "trailing_slash": UrlAppendTrailingSlashHandler
    }
    members_url: str
    token_url: str
    credential_url: str
    resource_url: str
    sdk_root: str = "/".join(os.path.realpath(__file__).split("/")[:-2])


def load_settings(**kwargs: str) -> Settings:
    return Settings()


settings = load_settings()
