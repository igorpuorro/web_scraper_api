from abc import ABC, abstractmethod
from typing import Any

from app.app_config.app_config import AppConfig


class BaseCache(ABC):
    def __init__(self, app_config: AppConfig):
        pass

    @abstractmethod
    def generate_cache_key(self, url: str) -> str:
        pass

    @abstractmethod
    def is_cached(self, url: str) -> bool:
        pass

    @abstractmethod
    def load_from_cache(self, url: str) -> Any:
        pass

    @abstractmethod
    def save_to_cache(self, url: str, content: Any) -> None:
        pass
