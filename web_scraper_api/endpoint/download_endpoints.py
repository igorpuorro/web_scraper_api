from typing import Dict, List

import json
import os

from werkzeug.exceptions import BadRequest
from flask import Blueprint, current_app, jsonify, request, send_file

blueprint_download_endpoints = Blueprint("download", __name__)


@blueprint_download_endpoints.route("/download/<filename>", methods=["GET"])
def endpoint_get_download(filename):
    file_path = os.path.join(
        os.path.abspath(
            current_app.app_config.get("chrome_download_default_directory")
        ),
        filename
    )

    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}, 404)


@blueprint_download_endpoints.route("/download/<filename>", methods=["DELETE"])
def endpoint_delete_download(filename):
    file_path = os.path.join(
        os.path.abspath(
            current_app.app_config.get("chrome_download_default_directory")
        ),
        filename
    )

    if os.path.isfile(file_path):
        os.remove(file_path)

        return jsonify({"message": "File deleted successfully", "filename": filename})
    else:
        return jsonify({"error": "File not found"}, 404)
