import datetime
import inspect
import logging
import os

from flask import request
from selenium.common.exceptions import WebDriverException

from app.app_config.app_config import AppConfig
from app.connector.base_connector import BaseConnector


class AppLogger:
    log_level: int
    screenshot_directory: str
    logger: logging.Logger

    def __init__(self, app_name: str, app_config: AppConfig):
        self.log_level = self.get_level_name(app_config.get("log_level"))
        log_directory = app_config.get("log_directory")
        self.screenshot_directory = app_config.get("screenshot_directory")

        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(self.log_level)

        log_format = "%(asctime)s - %(levelname)s - %(caller)s - %(message)s"
        log_formatter = logging.Formatter(log_format)

        log_file = os.path.join(log_directory, app_name)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_formatter)

        # stream_handler = logging.StreamHandler()
        # stream_handler.setFormatter(log_formatter)

        self.logger.addHandler(file_handler)
        # self.logger.addHandler(stream_handler)

    def get_level_name(self, log_level: str) -> int:
        try:
            return logging.getLevelName(log_level)

        except Exception as error:
            raise ValueError(error) from error

    def log(self, log_level: int, message: str) -> None:
        try:
            if log_level >= self.log_level:
                log_method_name = str(logging.getLevelName(log_level)).lower()
                log_function = getattr(self.logger, log_method_name)

                stack_frame = inspect.stack()[2]
                caller_class_name = stack_frame[0].f_locals["self"].__class__.__name__
                caller_method_name = stack_frame[0].f_code.co_name
                caller = f"{caller_class_name}.{caller_method_name}"

                if request:
                    request_remote_add = request.remote_addr
                    request_path = request.path
                    log_function(
                        f"{request_remote_add} - {request_path} - {message}",
                        extra={"caller": caller}
                    )
                else:
                    log_function(
                        f"{message}",
                        extra={"caller": caller}
                    )

        except (AttributeError, IndexError) as error:
            logging.error("Failed to log: %s", str(error))

    def log_screenshot(self, log_level: int, connector: BaseConnector) -> None:
        try:
            if log_level >= self.log_level:
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
                screenshot_filename = f"{timestamp}.png"
                screenshot_path = os.path.join(
                    self.screenshot_directory, screenshot_filename
                )

                getattr(
                    connector,
                    "driver"
                ).get_screenshot_as_file(screenshot_path)

                self.log(log_level, f"SCREENSHOT {screenshot_path}")

        except WebDriverException as error:
            logging.error("Failed to capture screenshot: %s", str(error))
