from typing import Dict, List

import json

from werkzeug.exceptions import BadRequest
from flask import Blueprint, current_app, jsonify, request

from app.extractor.job_search_extractor_factory import JobSearchExtractorFactory
from app.handler.selenium_job_search_handler_factory import SeleniumJobSearchHandlerFactory
from app.matching.advanced_matching import AdvancedMatching
from app.openapi import openapi
from app.presenter.keyword_presenter import KeywordPresenter


blueprint_keyword_endpoints = Blueprint("keyword", __name__)


@blueprint_keyword_endpoints.route("/keyword/match/summary", methods=["POST"])
@openapi
def endpoint_post_keyword_match_summary():
    try:
        request_data: Dict[str, str] = request.json
        url: str = request_data.get("url", "")
        keywords: List[str] = request_data.get("keywords", "[]")
        threshold: str = request_data.get("threshold", "")

        selenium_job_search_handler = SeleniumJobSearchHandlerFactory.create(
            current_app.selenium_connector,
            url
        )
        # selenium_job_search_handler.retrieve_content()
        selenium_job_search_handler.retrieve_cached_content()

        job_search_extractor = JobSearchExtractorFactory.create(
            selenium_job_search_handler,
            selenium_job_search_handler.find_section_job_description
        )
        job_search_extractor.extract_job_description()
        job_description = job_search_extractor.get_setences()

        matching = AdvancedMatching()
        summary = {}

        if len(threshold) == 0:
            summary = matching.match_with_sentences(
                job_description,
                keywords
            )
        else:
            summary = matching.match_with_sentences(
                job_description,
                keywords,
                threshold=int(threshold)
            )

        keyword_presenter = KeywordPresenter()
        response_data = keyword_presenter.format_summary(summary)
        response = jsonify(response_data)

        return response, 200

    except BadRequest as error:
        return jsonify({"error": error.description}), 400

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        return jsonify({"error": str(error)}), 500
