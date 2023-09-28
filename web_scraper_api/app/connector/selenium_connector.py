from typing import Union

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from app.app_config.app_config import AppConfig
from app.cache.base_cache import BaseCache
from app.connector.base_connector import BaseConnector


class SeleniumConnector(BaseConnector):
    chrome_path: str
    chromedriver_path: str
    driver: webdriver.Chrome

    def __init__(self, app_config: AppConfig, cache: Union[None, BaseCache] = None):
        super().__init__(app_config, cache)

        self.chrome_path = app_config.get("chrome_path")
        self.chromedriver_path = app_config.get("chromedriver_path")

    def connect(self) -> None:
        try:
            chrome_options = Options()
            chrome_options.add_argument(
                "--disable-blink-features=AutomationControlled")
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
            chrome_prefs = {
                "profile.default_content_setting_values": {"images": 0}
            }
            chrome_options.add_experimental_option("prefs", chrome_prefs)
            chrome_options.binary_location = self.chrome_path

            webdriver_service = Service(self.chromedriver_path)

            self.driver = webdriver.Chrome(
                service=webdriver_service,
                options=chrome_options
            )

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error

    def disconnect(self) -> None:
        try:
            self.driver.quit()

        except Exception as error:
            raise RuntimeError(
                f"{self.__class__.__qualname__}>\n{error}") from error
