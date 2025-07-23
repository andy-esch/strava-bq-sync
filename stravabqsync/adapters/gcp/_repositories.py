from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.adapters.gcp.schemas import STRAVA_ACTIVITY_SCHEMA
from stravabqsync.domain import StravaActivity
from stravabqsync.ports.out.write import WriteActivities


class WriteActivitiesRepo(WriteActivities):
    """Write Strava Activities to BigQuery"""

    def __init__(self, client: BigQueryClientWrapper, *, dataset_name: str):
        self._client = client
        self._dataset_name = dataset_name
        self._table_name = "activities"

    def write_activity(self, activity: StravaActivity) -> None:
        activities_dict = [activity.model_dump()]
        self._client.insert_rows_json(
            activities_dict,
            dataset_name=self._dataset_name,
            table_name=self._table_name,
        )

    def create_activities_table(self) -> None:
        """Create the BigQuery activities table with the Strava Activity schema."""
        table_id = f"{self._client.project_id}.{self._dataset_name}.{self._table_name}"
        self._client.create_table(table_id, schema=STRAVA_ACTIVITY_SCHEMA)
