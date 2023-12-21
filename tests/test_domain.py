import json

import pytest

from stravabqsync.domain import StravaActivity


@pytest.fixture
def activity_json_1():
    with open("tests/fixtures/activity_1.json", "r", encoding="utf-8") as fin:
        activity = json.load(fin)
    return activity


@pytest.fixture
def activity_json_2():
    with open("tests/fixtures/activity_2.json", "r", encoding="utf-8") as fin:
        activity = json.load(fin)
    return activity


class TestStravaActivity:
    def test_strava_activity_id_1(self, activity_json_1):
        activity = StravaActivity(**activity_json_1)

        assert activity.id == 12345678987654321

    def test_strava_activity_id_2(self, activity_json_2):
        activity = StravaActivity(**activity_json_2)

        assert activity.id == 8726373550
