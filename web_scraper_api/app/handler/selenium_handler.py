import json
import time

from app.connector.selenium_connector import SeleniumConnector
from app.handler.base_handler import BaseHandler


class SeleniumHandler(BaseHandler):
    connector: SeleniumConnector

    def __init__(self, connector: SeleniumConnector, url: str):
        super().__init__(connector, url)

    def browser_navigator_object(self) -> str:
        try:
            navigator = self.connector.driver.execute_script(
                """
                return {
                    appCodeName: navigator.appCodeName,
                    appName: navigator.appName,
                    appVersion: navigator.appVersion,
                    buildId: navigator.buildId,
                    connection: navigator.connection,
                    cookieEnabled: navigator.cookieEnabled,
                    doNotTrack: navigator.doNotTrack,
                    geolocation: navigator.geolocation,
                    globalPrivacyControl: navigator.globalPrivacyControl,
                    javaEnabled: navigator.javaEnabled(),
                    language: navigator.language,
                    onLine: navigator.onLine,
                    permissions: navigator.permissions,
                    platform: navigator.platform,
                    plugins: Array.from(navigator.plugins).map(p => ({
                        name: p.name,
                        filename: p.filename
                    })),
                    product: navigator.product,
                    productSub: navigator.productSub,
                    securitypolicy: navigator.securitypolicy,
                    userAgent: navigator.userAgent,
                    userAgentData: navigator.userAgentData,
                    vendor: navigator.vendor,
                    vendorSub: navigator.vendorSub,
                    webdriver: navigator.webdriver
                };
                """
            )

            return json.dumps(navigator, indent=4)

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

    def retrieve_cached_content(self) -> None:
        try:
            cached_content = self.cache.load_from_cache(self.url)

            if cached_content:
                self.connector.driver.get("about:blank")
                self.connector.driver.execute_script(
                    "document.write(arguments[0]);",
                    cached_content
                )
                self.connector.driver.execute_script(
                    "document.close();"
                )

                time.sleep(1)

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

    def take_screenshot(self, screenshot_path: str) -> None:
        try:
            driver = getattr(self.connector, "driver")

            height = driver.execute_script(
                "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"
            )
            width = driver.execute_script(
                "return Math.max( document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth );"
            )

            driver.set_window_size(width, height)

            driver.execute_script(
                "window.scrollTo(0, window.scrollY + window.innerHeight);"
            )

            driver.save_screenshot(screenshot_path)

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
