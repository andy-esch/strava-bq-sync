import json
from functools import lru_cache

import pytest

from stravabqsync.application.services._sync_service import SyncService
from stravabqsync.domain import StravaActivity, StravaTokenSet
from tests.mocks.read_activities_repo import MockReadActivitiesRepo
from tests.mocks.read_token_repo import MockStravaTokenRepo
from tests.mocks.write_activities import MockWriteActivitesRepo


def _activity():
    with open("tests/fixtures/activity_2.json", "r", encoding="utf-8") as fin:
        activity = json.load(fin)
    # NOTE: id = 8726373550
    return StravaActivity(**activity)


@pytest.fixture
def activity():
    return _activity()


def mock_token_repo():
    tokenset = StravaTokenSet(
        client_id=1, client_secret="foo", refresh_token="bar", access_token="baz"
    )
    return MockStravaTokenRepo(tokenset)


def mock_read_activities_repo(tokens: StravaTokenSet):
    return MockReadActivitiesRepo(_activity())


@lru_cache(maxsize=1)
def mock_write_activities_repo():
    return MockWriteActivitesRepo()


@pytest.fixture
def service():
    return SyncService(
        read_strava_token=mock_token_repo,
        read_activities=mock_read_activities_repo,
        write_activities=mock_write_activities_repo,
    )


class TestSyncService:
    def test_usage(self, service, activity):
        service.run(activity)
        assert service._write_activities.activity.id == 8726373550
