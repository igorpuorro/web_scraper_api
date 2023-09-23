import os
import json

from flask import current_app


class AppConfig:
    app_name: str

    def __init__(self, app_name: str, config_file_path: str):
        self.app_name = app_name

        config = self._load_json(config_file_path)
        current_app.config.update(config)

        self._create_directories(app_name)

    def _create_directories(self, app_name: str) -> None:
        app_name_key = current_app.config.get(app_name)

        if app_name_key:
            for key, value in app_name_key.items():
                if "_directory" in key:
                    directory_path = os.path.abspath(value)
                    os.makedirs(directory_path, exist_ok=True)

    def _load_json(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)

        return content

    def get(self, key: str, default=None):
        try:
            app_name_key = current_app.config.get(self.app_name)

            if app_name_key:
                value = app_name_key.get(key, default)

                return value

        except Exception as error:
            raise ValueError(error) from error
