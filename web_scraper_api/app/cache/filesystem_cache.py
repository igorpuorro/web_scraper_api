from typing import Any

import os
import hashlib
import pickle

from app.cache.base_cache import BaseCache


class FilesystemCache(BaseCache):
    def __init__(self, config: dict):
        super().__init__(config)

        if not os.path.exists(self.config["cache_directory"]):
            raise FileNotFoundError(self.config["cache_directory"])

    def generate_cache_key(self, url: str) -> str:
        return hashlib.md5(url.encode("utf-8")).hexdigest()

    def is_cached(self, url) -> bool:
        cache_key = self.generate_cache_key(url)
        cache_file_path = os.path.join(
            self.config["cache_directory"], cache_key)

        return os.path.exists(cache_file_path)

    def load_from_cache(self, url) -> Any:
        if self.is_cached(url):
            cache_key = self.generate_cache_key(url)
            cache_file_path = os.path.join(
                self.config["cache_directory"], cache_key)

            with open(cache_file_path, "rb") as cache_file:
                return pickle.load(cache_file)

        return None

    def save_to_cache(self, url, content) -> None:
        cache_key = self.generate_cache_key(url)
        cache_file_path = os.path.join(
            self.config["cache_directory"], cache_key)

        with open(cache_file_path, "wb") as cache_file:
            pickle.dump(content, cache_file)
