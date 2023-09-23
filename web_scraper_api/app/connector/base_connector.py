from abc import ABC
from typing import Union

from app.app_config.app_config import AppConfig
from app.cache.base_cache import BaseCache


class BaseConnector(ABC):
    cache: Union[None, BaseCache]

    def __init__(self, app_config: AppConfig, cache: Union[None, BaseCache] = None):
        pass
