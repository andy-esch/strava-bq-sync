import json
from functools import lru_cache

import pytest

from stravabqsync.adapters.gcp._repositories import WriteActivitiesRepo
from stravabqsync.domain import StravaActivity
from tests.mocks.bigquery_client_wrapper import MockBigQueryClientWrapper


@lru_cache(maxsize=1)
def bq_client():
    return MockBigQueryClientWrapper(project_id="test-project")


@pytest.fixture
def activity2():
    with open("tests/fixtures/activity_2.json", "r", encoding="utf-8") as fin:
        activity = json.load(fin)
    return StravaActivity(**activity)


@pytest.fixture
def write_activities_repo():
    return WriteActivitiesRepo(bq_client(), dataset_name="test-dataset")


class TestWriteActivitiesRepo:
    def test_insert_activity_dataset_name(self, write_activities_repo, activity2):
        write_activities_repo.write_activity(activity2)
        assert write_activities_repo._client.dataset_name == "test-dataset"

    def test_insert_activity_activity_written(self, write_activities_repo, activity2):
        write_activities_repo.write_activity(activity2)
        assert isinstance(write_activities_repo._client.written_activities, list)

    def test_insert_activity_activity_written_row(
        self, write_activities_repo, activity2
    ):
        write_activities_repo.write_activity(activity2)
        assert isinstance(write_activities_repo._client.written_activities[0], dict)

    def test_create_activities_table(self, write_activities_repo):
        write_activities_repo.create_activities_table()
        expected_table_id = "test-project.test-dataset.activities"
        assert write_activities_repo._client.table_id == expected_table_id
