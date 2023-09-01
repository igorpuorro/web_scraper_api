from typing import Callable

from app.extractor.job_search_extractor import JobSearchExtractor
from app.extractor.job_search_glassdoor_extractor import JobSearchGlassdoorExtractor
from app.extractor.job_search_linkedin_extractor import JobSearchLinkedInExtractor
from app.handler.base_handler import BaseHandler
from app.handler.selenium_job_search_glassdoor_handler import SeleniumJobSearchGlassdoorHandler
from app.handler.selenium_job_search_linkedin_handler import SeleniumJobSearchLinkedInHandler


class JobSearchExtractorFactory:
    @staticmethod
    def create(handler: BaseHandler, method: Callable[[], str]) -> JobSearchExtractor:
        if isinstance(handler, SeleniumJobSearchGlassdoorHandler):
            return JobSearchGlassdoorExtractor(method())
        elif isinstance(handler, SeleniumJobSearchLinkedInHandler):
            return JobSearchLinkedInExtractor(method())
        else:
            raise ValueError("Unsupported type.")
