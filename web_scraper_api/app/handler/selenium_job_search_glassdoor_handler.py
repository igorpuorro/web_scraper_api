from flask import current_app

from app.handler.selenium_job_search_handler import SeleniumJobSearchHandler


class SeleniumJobSearchGlassdoorHandler(SeleniumJobSearchHandler):
    def find_section_job_description(self) -> str:
        try:
            getattr(current_app, "app_logger").log_screenshot(
                getattr(current_app, "app_logger").get_level_name("INFO"),
                self
            )

            return self.connector.driver.page_source

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
