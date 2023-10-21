import os

from flask import Blueprint, current_app, jsonify, send_file


blueprint_download_endpoints = Blueprint("download", __name__)


@blueprint_download_endpoints.route("/download/<filename>", methods=["GET"])
def endpoint_get_download(filename):
    file_path = os.path.join(
        current_app.app_config.get("chrome_download_default_directory"),
        filename
    )

    if os.path.isfile(file_path):
        response = send_file(
            file_path, as_attachment=True
        )
        response.direct_passthrough = False

        return response, 200

    else:
        return jsonify(
            {"error": "File not found"}
        ), 404


@blueprint_download_endpoints.route("/download/<filename>", methods=["DELETE"])
def endpoint_delete_download(filename):
    file_path = os.path.join(
        current_app.app_config.get("chrome_download_default_directory"),
        filename
    )

    if os.path.isfile(file_path):
        os.remove(file_path)

        return jsonify(
            {"message": "File deleted successfully"}
        ), 204
    else:
        return jsonify(
            {"error": "File not found"}
        ), 404
