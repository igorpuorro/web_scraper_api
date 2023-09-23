from app.connector.selenium_connector import SeleniumConnector
from app.handler.base_handler import BaseHandler


class SeleniumHandler(BaseHandler):
    connector: SeleniumConnector

    def __init__(self, connector: SeleniumConnector, url: str):
        super().__init__(connector, url)

    def retrieve_cached_content(self) -> None:
        try:
            cached_content = self.cache.load_from_cache(self.url)

            if cached_content:
                self.connector.driver.get("about:blank")
                self.connector.driver.execute_script(
                    "document.body.innerHTML = arguments[0];",
                    cached_content
                )
            else:
                self.retrieve_content()

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

    def retrieve_content(self) -> None:
        try:
            self.connector.driver.get("chrome://version/")
            self.connector.driver.get(self.url)

            if not self.cache.is_cached(self.url):
                self.cache.save_to_cache(
                    self.url,
                    self.connector.driver.page_source
                )

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
