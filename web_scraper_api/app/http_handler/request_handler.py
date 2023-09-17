from typing import Any, Dict

import json

from werkzeug.exceptions import BadRequest
from flask import Request


class RequestHandler:
    @staticmethod
    def validate_request(request: Request) -> Dict[str, Any]:
        if request.content_type != "application/json":
            raise BadRequest("Request content type must be 'application/json'")

        if not request.data:
            raise BadRequest("Empty request body")

        try:
            request_data = request.json

        except json.JSONDecodeError:
            raise BadRequest("Invalid JSON data in the request body")

        return request_data

    @staticmethod
    def validate_request_data(data: Dict[str, Any], mandatory_keys: Dict[str, Any]) -> None:
        error_messages = []

        for key, expected_type in mandatory_keys.items():
            if key not in data:
                error_messages.append(f"The '{key}' field is missing")

            elif not isinstance(data[key], expected_type):
                error_messages.append(
                    f"The '{key}' field should be of type {expected_type.__name__}")

        if error_messages:
            raise BadRequest(error_messages)
