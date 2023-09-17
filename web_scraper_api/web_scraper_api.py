import atexit
import datetime
import os
import yaml

from flask import Flask
from flask_cors import CORS
import nltk

from app.connector.selenium_connector import SeleniumConnector

from endpoint.keyword_endpoints import blueprint_keyword_endpoints


def cleanup_function():
    with app.app_context():
        if hasattr(app, 'selenium_connector') and isinstance(app.selenium_connector, SeleniumConnector):
            app.selenium_connector.disconnect()


def load_yaml(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as yaml_file:
        content = yaml.safe_load(yaml_file)
    return content


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
            config_yaml = load_yaml(os.path.join("config", "config.yaml"))
            app_instance.config.update(config_yaml)

            cache_directory = app_instance.config.get(
                "web_scraper_api").get("cache_directory")
            os.makedirs(cache_directory, exist_ok=True)

            nltk_download_punkt()

            selenium_connector = SeleniumConnector(app_instance.config)

            if not selenium_connector:
                raise RuntimeError("Failed to create SeleniumConnector")

            selenium_connector.connect()
            app_instance.selenium_connector = selenium_connector

    except Exception as error:
        raise RuntimeError(error) from error

    return app_instance


app = create_app()

atexit.register(cleanup_function)
CORS(app, origins=["*"])

app.register_blueprint(blueprint_keyword_endpoints)
