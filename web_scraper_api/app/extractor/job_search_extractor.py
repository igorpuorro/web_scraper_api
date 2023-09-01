from abc import abstractmethod

from app.extractor.base_extractor import BaseExtractor


class JobSearchExtractor(BaseExtractor):
    @abstractmethod
    def extract_job_description(self) -> None:
        pass
