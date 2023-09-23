from flask import current_app
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.handler.selenium_job_search_handler import SeleniumJobSearchHandler


class SeleniumJobSearchLinkedInHandler(SeleniumJobSearchHandler):
    def find_section_job_description(self) -> str:
        page_source: str

        try:
            locator = (By.CLASS_NAME, "show-more-less-html__button")
            element = WebDriverWait(self.connector.driver, 10).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            # self.connector.driver.execute_script(
            #    "window.scrollTo(0, document.body.scrollHeight);"
            # )
            page_source = self.connector.driver.page_source

            getattr(current_app, "app_logger").log_screenshot(
                getattr(current_app, "app_logger").get_level_name("INFO"),
                self.connector
            )

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

        return page_source
