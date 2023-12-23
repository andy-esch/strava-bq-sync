"""Test script for testing Strava webhooks"""
import base64
import json
import logging

import functions_framework
from cloudevents.http import CloudEvent

from stravabqsync.application.services import make_sync_service
from stravabqsync.domain import WebhookRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.cloud_event
def stravabqsync_listener(event: CloudEvent) -> dict:
    """main runner"""
    logger.info("Received event: %s", str(event.data))
    event_data = json.loads(base64.b64decode(event.data["message"]["data"]).decode())
    parsed_request = WebhookRequest(**event_data)
    logger.info("Parsed event: %s", parsed_request.json())

    if parsed_request.aspect_type == "create":
        usecase = make_sync_service()
        usecase.run(parsed_request.object_id)
    else:
        logger.info("Skipping non-create events: %s", parsed_request.updates)

    return parsed_request.json()
