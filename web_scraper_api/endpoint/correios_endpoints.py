from typing import Dict, List

import json

from werkzeug.exceptions import BadRequest
from flask import Blueprint, current_app, jsonify, request

from app.handler.selenium_correios_handler_factory import SeleniumCorreiosHandlerFactory
from app.openapi import openapi


blueprint_correios_endpoints = Blueprint("correios", __name__)


@blueprint_correios_endpoints.route("/correios/enderecador/encomendas", methods=["POST"])
@openapi
def endpoint_post_correios_enderecador_encomendas():
    try:
        request_data_latin1 = request.data.decode("utf-8").encode("latin-1")

        request_data: Dict[str, str] = json.loads(
            request_data_latin1.decode("latin-1")
        )

        remetente: Dict[str, str] = request_data.get("remetente", "{}")
        destinatario: List[dict] = request_data.get("destinatario", "[]")

        url = "https://www2.correios.com.br/enderecador/encomendas/default.cfm"

        selenium_correios_enderecador_encomendas_handler = SeleniumCorreiosHandlerFactory.create(
            current_app.selenium_connector,
            url
        )

        selenium_correios_enderecador_encomendas_handler.retrieve_content()

        pdf_list = selenium_correios_enderecador_encomendas_handler.enderecador_encomendas(
            remetente, destinatario
        )

        response_data = {
            "pdf_list": pdf_list
        }

        response = jsonify(response_data)

        return response, 200

    except BadRequest as error:
        return jsonify({"error": error.description}), 400

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        return jsonify({"error": str(error)}), 500
