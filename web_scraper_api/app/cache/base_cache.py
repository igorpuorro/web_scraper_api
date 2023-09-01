from abc import ABC


class BaseCache(ABC):
    config: dict

    def __init__(self, config: dict):
        self.config = config
