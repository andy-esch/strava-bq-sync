"""Test script for testing Strava webhooks"""
import json
import logging

import functions_framework
from flask import Request

from stravabqsync.application.services import make_sync_service
from stravabqsync.domain import WebhookRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def stravabqsync_listener(request: Request) -> dict:
    """main runner"""
    if request.method == "POST":
        logger.info("Received event: %s", str(request.json))
        parsed_request = WebhookRequest(**request.json)
        logger.info("Parsed event: %s", parsed_request.json())

        if parsed_request.aspect_type == "create":
            usecase = make_sync_service()
            usecase.run(parsed_request.object_id)
        else:
            logger.info("Skipping non-create events: %s", parsed_request.updates)

        return parsed_request.json()
    elif request.method == "GET":
        # Needed to register callback with Strava Webhook
        return json.dumps({"hub.challenge": request.args["hub.challenge"]})

    raise ValueError(
        f"""Cannot handle request:
            args={json.dumps(request.args)}
            data={request.json}
            method={request.method}
        """
    )
