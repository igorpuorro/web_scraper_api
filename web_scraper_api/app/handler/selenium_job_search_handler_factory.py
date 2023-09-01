from app.connector.base_connector import BaseConnector
from app.handler.selenium_job_search_handler import SeleniumJobSearchHandler
from app.handler.selenium_job_search_glassdoor_handler import SeleniumJobSearchGlassdoorHandler
from app.handler.selenium_job_search_linkedin_handler import SeleniumJobSearchLinkedInHandler


class SeleniumJobSearchHandlerFactory:
    @staticmethod
    def create(connector: BaseConnector, url: str) -> SeleniumJobSearchHandler:
        if ".glassdoor.com" in url:
            return SeleniumJobSearchGlassdoorHandler(connector, url)
        elif ".linkedin.com" in url:
            return SeleniumJobSearchLinkedInHandler(connector, url)
        else:
            raise ValueError("Unsupported URL.")
