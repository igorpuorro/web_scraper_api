import atexit
import datetime
import os

from flask import Flask
from flask_cors import CORS
import nltk
from swagger_ui import api_doc

from app.app_config.app_config import AppConfig
from app.app_logger.app_logger import AppLogger
from app.cache.filesystem_cache import FilesystemCache
from app.connector.selenium_connector import SeleniumConnector

from endpoint.correios_endpoints import blueprint_correios_endpoints
from endpoint.download_endpoints import blueprint_download_endpoints
from endpoint.keyword_endpoints import blueprint_keyword_endpoints


def cleanup_function():
    with app.app_context():
        if hasattr(app, 'selenium_connector') and isinstance(getattr(app, "selenium_connector"), SeleniumConnector):
            getattr(
                app,
                "selenium_connector"
            ).disconnect()


def nltk_download_punkt(force: bool = False) -> None:
    try:
        nltk_data_directory = nltk.data.find("")
        punkt_zip_file = os.path.join(
            nltk_data_directory, "tokenizers", "punkt.zip")

        last_modification_time = datetime.datetime.fromtimestamp(
            os.path.getmtime(punkt_zip_file)
        )
        current_time = datetime.datetime.now()
        time_difference = current_time - last_modification_time

        days_since_last_download = 1

        if force or time_difference.total_seconds() > days_since_last_download * 86400:
            nltk.download("punkt")

            current_timestamp = int(current_time.timestamp())
            os.utime(punkt_zip_file, (current_timestamp, current_timestamp))

    except LookupError:
        nltk.download("punkt")


def create_app():
    app_instance = Flask(__name__)

    try:
        with app_instance.app_context():
            setattr(
                app_instance,
                "app_config",
                AppConfig(__name__, os.path.join("config", "config.json"))
            )

            if not hasattr(app_instance, "app_config"):
                raise RuntimeError("Failed to create AppConfig")

            setattr(
                app_instance,
                "app_logger",
                AppLogger(__name__, getattr(app_instance, "app_config"))
            )

            if not hasattr(app_instance, "app_logger"):
                raise RuntimeError("Failed to create Logger")

            openapi_path = getattr(
                app_instance, "app_config").get("openapi_path")

            api_doc(
                app_instance,
                config_path=f"{openapi_path}",
                url_prefix="/api/doc",
                title="Web Scraper API"
            )

            nltk_download_punkt()

            setattr(
                app_instance,
                "selenium_connector",
                SeleniumConnector(
                    getattr(app_instance, "app_config"),
                    FilesystemCache(getattr(app_instance, "app_config"))
                )
            )

            if not hasattr(app_instance, "selenium_connector"):
                raise RuntimeError("Failed to create SeleniumConnector")

            getattr(app_instance, "selenium_connector").connect()

    except Exception as error:
        raise RuntimeError(error) from error

    return app_instance


app = create_app()

atexit.register(cleanup_function)
CORS(app, origins=["*"])

app.register_blueprint(blueprint_correios_endpoints)
app.register_blueprint(blueprint_download_endpoints)
app.register_blueprint(blueprint_keyword_endpoints)
