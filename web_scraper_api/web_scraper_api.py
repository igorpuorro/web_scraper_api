from typing import Optional

import atexit
import datetime
import os
import yaml

from flask import current_app, Flask
from flask_cors import CORS
import nltk

from app.connector.selenium_connector import SeleniumConnector

from endpoint.keyword_endpoints import blueprint_keyword_endpoints


def cleanup_function():
    with app.app_context():
        if "selenium_connector" in current_app.config:
            current_app.config["selenium_connector"].disconnect()


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
        days_since_last_download = 5

        if force or time_difference.total_seconds() > days_since_last_download * 86400:
            nltk.download("punkt")

    except LookupError:
        nltk.download("punkt")


def create_app():
    config: Optional[dict] = None
    selenium_connector: Optional[SeleniumConnector] = None

    app_instance = Flask(__name__)

    with app_instance.app_context():
        try:
            config = load_yaml(
                os.path.join("config", "config.yaml"))

            if isinstance(config, dict):
                if "cache_directory" in config:
                    if not os.path.exists(config["cache_directory"]):
                        os.makedirs(config["cache_directory"])

                selenium_connector = SeleniumConnector(config)

            if isinstance(selenium_connector, SeleniumConnector):
                selenium_connector.connect()
                current_app.config["config"] = config
                current_app.config["selenium_connector"] = selenium_connector

            nltk_download_punkt()

        except Exception as error:
            raise RuntimeError(error) from error

    return app_instance


app = create_app()

atexit.register(cleanup_function)
CORS(app, origins=["*"])

app.register_blueprint(blueprint_keyword_endpoints)
