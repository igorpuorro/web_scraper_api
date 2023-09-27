from flask import current_app

from app.handler.selenium_job_search_handler import SeleniumJobSearchHandler


class SeleniumJobSearchLinkedInHandler(SeleniumJobSearchHandler):
    def find_section_job_description(self) -> str:
        try:
            self.connector.driver.execute_script(
                '''
                const xpathExpression = '/html/body/main/section[1]/div/div/section[1]/div/div/section/button[1]';
                const element = document.evaluate(xpathExpression, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;

                if (element) {
                    element.addEventListener('click', function() {
                        console.log('Button clicked!');
                    });

                    element.click();
                }
                '''
            )

            getattr(current_app, "app_logger").log_screenshot(
                getattr(current_app, "app_logger").get_level_name("INFO"),
                self
            )

            getattr(current_app, "app_logger").log_browser_navigator_object(
                getattr(current_app, "app_logger").get_level_name("INFO"),
                self
            )

            return self.connector.driver.page_source

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
