from abc import ABC


class BaseConnector(ABC):
    config: dict

    def __init__(self, config: dict):
        self.config = config
