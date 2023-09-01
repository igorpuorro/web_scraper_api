from abc import ABC

from langdetect import detect
from nltk.tokenize import sent_tokenize


class BaseExtractor(ABC):
    content: str

    def __init__(self, content: str):
        self.content = content

    def get_raw(self) -> str:
        if not self.content:
            raise ValueError(f"{self.__class__.__qualname__}>")

        return self.content

    def get_setences(self) -> list:
        if not self.content:
            raise ValueError(f"{self.__class__.__qualname__}>")

        try:
            language_detected = detect(self.content)
            language_mapping = {"es": "spanish", "pt": "portuguese"}
            language = language_mapping.get(language_detected, "english")

            return sent_tokenize(self.content, language=language)

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
