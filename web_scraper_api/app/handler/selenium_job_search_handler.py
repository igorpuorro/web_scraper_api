from abc import abstractmethod

from app.handler.selenium_handler import SeleniumHandler


class SeleniumJobSearchHandler(SeleniumHandler):
    @abstractmethod
    def find_section_job_description(self) -> str:
        pass
