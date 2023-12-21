"""Strava read repositories"""
# pylint: disable=too-few-public-methods
import logging
from functools import cached_property

import requests

from stravabqsync.domain import StravaActivity, StravaTokenSet
from stravabqsync.ports.out.read import ReadActivities, ReadStravaToken

logger = logging.getLogger(__name__)


class StravaTokenRepo(ReadStravaToken):
    """Fetch new access token"""

    def __init__(self, tokens: StravaTokenSet):
        self._tokens = tokens
        self._url = "https://www.strava.com/oauth/token"

    @cached_property
    def refresh(self) -> StravaTokenSet:
        payload = {
            "client_id": self._tokens.client_id,
            "client_secret": self._tokens.client_secret,
            "refresh_token": self._tokens.refresh_token,
            "grant_type": "refresh_token",
        }
        resp = requests.post(url=self._url, data=payload, timeout=10)

        if resp.ok:
            access_token = resp.json()["access_token"]
            logger.info("Tokens successfully updated")
            return StravaTokenSet(
                client_id=self._tokens.client_id,
                client_secret=self._tokens.client_secret,
                access_token=access_token,
                refresh_token=self._tokens.refresh_token,
            )
        raise resp.raise_for_status()


class StravaActivitiesRepo(ReadActivities):
    """Repository for fetching Strava Activities"""

    def __init__(self, tokens: StravaTokenSet):
        self._tokens = tokens
        self._headers = {"Authorization": f"Bearer {self._tokens.access_token}"}
        self._activity_endpoint = (
            "https://www.strava.com/api/v3/activities/{activity_id}"
        )
        self._activities_endpoint = "https://www.strava.com/api/v3/activities"

    def _read_raw_activity_by_id(self, activity_id: int) -> dict:
        resp = requests.get(
            url=self._activity_endpoint.format(activity_id=activity_id),
            headers=self._headers,
            timeout=10,
        )
        if not resp.ok:
            raise resp.raise_for_status()
        return resp.json()

    def read_activity_by_id(self, activity_id: int) -> StravaActivity:
        resp = self._read_raw_activity_by_id(activity_id)
        activity = StravaActivity(**resp)
        return activity
