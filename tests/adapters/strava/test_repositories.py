import json

import pytest
from requests_mock import Mocker

from stravabqsync.adapters.strava._repositories import (
    StravaActivitiesRepo,
    StravaTokenRepo,
)
from stravabqsync.domain import StravaActivity, StravaTokenSet
from stravabqsync.exceptions import ActivityNotFoundError, StravaTokenError


@pytest.fixture
def tokenset():
    return StravaTokenSet(
        client_id=1, client_secret="foo", refresh_token="bar", access_token=None
    )


@pytest.fixture
def activity_json():
    with open("tests/fixtures/activity_1.json", "r", encoding="utf-8") as fin:
        activity_json = json.load(fin)
    # NOTE: id = 12345678987654321
    return activity_json


@pytest.fixture
def token_repo(tokenset):
    return StravaTokenRepo(tokens=tokenset)


@pytest.fixture
def activities_repo(tokenset):
    return StravaActivitiesRepo(tokenset._replace(access_token="baz"))


class TestStravaTokenRepo:
    def test_refresh(self, token_repo):
        with Mocker() as m:
            m.post(token_repo._url, json={"access_token": "baz"})
            expected = token_repo.refresh
            assert expected.access_token == "baz"

    def test_failed_request(self, token_repo):
        with Mocker() as m:
            m.post(token_repo._url, status_code=401)

            with pytest.raises(StravaTokenError):
                token_repo.refresh


class TestStravaActivitiesRepo:
    def test_read_activity_by_id(self, activities_repo, activity_json):
        activity_id = 12345678987654321
        with Mocker() as m:
            m.get(
                activities_repo._activity_endpoint.format(activity_id=activity_id),
                json=activity_json,
            )
            resp = activities_repo.read_activity_by_id(activity_id)

        assert resp.id == activity_id

    def test_read_activity_by_id_type(self, activities_repo, activity_json):
        activity_id = 12345678987654321
        with Mocker() as m:
            m.get(
                activities_repo._activity_endpoint.format(activity_id=activity_id),
                json=activity_json,
            )
            resp = activities_repo.read_activity_by_id(activity_id)

        assert isinstance(resp, StravaActivity)

    def test_read_activity_not_found(self, activities_repo, activity_json):
        activity_id = -10
        with Mocker() as m:
            m.get(
                activities_repo._activity_endpoint.format(activity_id=activity_id),
                status_code=404,
            )
            with pytest.raises(ActivityNotFoundError):
                _ = activities_repo.read_activity_by_id(activity_id)
