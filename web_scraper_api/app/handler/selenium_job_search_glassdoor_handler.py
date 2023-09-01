from app.handler.selenium_job_search_handler import SeleniumJobSearchHandler


class SeleniumJobSearchGlassdoorHandler(SeleniumJobSearchHandler):
    def find_section_job_description(self) -> str:
        page_source: str

        try:
            page_source = self.connector.driver.page_source

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

        return page_source
