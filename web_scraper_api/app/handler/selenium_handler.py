from app.cache.filesystem_cache import FilesystemCache
from app.connector.selenium_connector import SeleniumConnector
from app.handler.base_handler import BaseHandler


class SeleniumHandler(BaseHandler):
    connector: SeleniumConnector

    def retrieve_cached_content(self) -> None:
        try:
            filesystem_cache = FilesystemCache(self.connector.config)
            cached_content = filesystem_cache.load_from_cache(self.url)

            if cached_content:
                self.connector.driver.get("about:blank")
                self.connector.driver.execute_script(
                    "document.body.innerHTML = arguments[0];", cached_content
                )
            else:
                self.retrieve_content()
                filesystem_cache.save_to_cache(
                    self.url, self.connector.driver.page_source)

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

    def retrieve_content(self) -> None:
        try:
            self.connector.driver.get("chrome://version/")
            self.connector.driver.get(self.url)

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
