from abc import ABC, abstractmethod

from app.connector.base_connector import BaseConnector


class BaseHandler(ABC):
    connector: BaseConnector
    url: str

    def __init__(self, connector: BaseConnector, url: str):
        self.connector = connector
        self.url = url

    @abstractmethod
    def retrieve_cached_content(self) -> None:
        pass

    @abstractmethod
    def retrieve_content(self) -> None:
        pass
