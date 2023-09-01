import json

from flask import Blueprint, current_app, jsonify, request

from app.extractor.job_search_extractor_factory import JobSearchExtractorFactory
from app.handler.selenium_job_search_handler_factory import SeleniumJobSearchHandlerFactory
from app.matching.advanced_matching import AdvancedMatching
from app.presenter.keyword_presenter import KeywordPresenter

blueprint_keyword_endpoints = Blueprint("keyword", __name__)


@blueprint_keyword_endpoints.route("/keyword/match/summary", methods=["POST"])
def endpoint_post_keyword_match_summary():
    url: str
    json_keywords: str

    try:
        url = str(request.args.get("url"))
        json_keywords = str(request.args.get("keywords"))
        keywords = json.loads(json_keywords)["keywords"]

        job_search_handler_factory = SeleniumJobSearchHandlerFactory()
        job_search_selenium_handler = job_search_handler_factory.create(
            current_app.config["selenium_connector"], url)
        # selenium_handler.retrieve_content()
        job_search_selenium_handler.retrieve_cached_content()

        job_search_extractor_factory = JobSearchExtractorFactory()
        job_search_extractor = job_search_extractor_factory.create(
            job_search_selenium_handler, job_search_selenium_handler.find_section_job_description
        )
        job_search_extractor.extract_job_description()
        job_description = job_search_extractor.get_setences()

        matching = AdvancedMatching()
        summary = matching.match_with_sentences(job_description, keywords)

        keyword_presenter = KeywordPresenter()
        response_data = keyword_presenter.format_summary(summary)
        response = jsonify(response_data)

        return response, 200

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        response = jsonify(message=error)

        return response, 500
