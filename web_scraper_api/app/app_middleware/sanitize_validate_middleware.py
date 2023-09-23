from typing import Callable

import json
from io import BytesIO

import jsonschema
from flask import Flask

from app.app_config.app_config import AppConfig


class SanitizeValidateMiddleware:
    api_contracts: dict
    app: Flask

    def __init__(self, app_config: AppConfig, app: Flask):
        self.api_contracts = self._load_json(
            app_config.get("api_contracts_path")
        )
        self.app = app

    def __call__(self, environ: dict, start_response: Callable[[str, list], None]):
        content_type = environ.get('CONTENT_TYPE', '').lower()

        if "application/json" not in content_type:
            response_body = json.dumps(
                {"error": "Content-Type must be application/json"}
            )
            start_response(
                "400 Bad Request",
                [("Content-Type", "application/json")]
            )

            return [response_body.encode('utf-8')]

        wsgi_input = environ.get("wsgi.input")

        if wsgi_input is not None:
            data = wsgi_input.read()
            sanitized_data = self._sanitize(data)

            # Replace the original request data with sanitized data
            environ["wsgi.input"] = BytesIO(sanitized_data)

        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")

        if path in self.api_contracts and method in self.api_contracts[path]:
            contract = self.api_contracts[path][method]

            if "schema" in contract:
                request_data = json.loads(sanitized_data.decode("utf-8"))

                if not self._validate_request_data(contract["schema"], request_data):
                    response_body = json.dumps(
                        {"error": "Invalid request data"}
                    )
                    start_response(
                        "400 Bad Request",
                        [("Content-Type", "application/json")]
                    )

                    return [response_body.encode("utf-8")]

        # Call the next middleware or the Flask app
        return self.app(environ, start_response)

    def _load_json(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as json_file:
            content = json.load(json_file)

        return content

    def _sanitize(self, data: bytes) -> bytes:
        return data

    def _validate_request_data(self, schema: dict, data: dict) -> bool:
        try:
            jsonschema.validate(data, schema)

            return True

        except jsonschema.exceptions.ValidationError:
            return False
