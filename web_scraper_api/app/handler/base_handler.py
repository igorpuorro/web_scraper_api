from abc import ABC, abstractmethod
from typing import Union

from app.cache.base_cache import BaseCache
from app.connector.base_connector import BaseConnector


class BaseHandler(ABC):
    connector: BaseConnector
    cache: Union[None, BaseCache]
    url: str

    def __init__(self, connector: BaseConnector, url: str):
        self.connector = connector
        self.cache = getattr(connector, "cache", None)
        self.url = url

    @abstractmethod
    def browser_navigator_object(self) -> str:
        pass

    @abstractmethod
    def retrieve_cached_content(self) -> None:
        pass

    @abstractmethod
    def retrieve_content(self) -> None:
        pass

    @abstractmethod
    def take_screenshot(self, screenshot_path: str) -> None:
        pass
