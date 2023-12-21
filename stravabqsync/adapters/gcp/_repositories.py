import json

from google.cloud.bigquery import SchemaField

from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.domain import StravaActivity
from stravabqsync.ports.out.write import WriteActivity


class WriteActivityRepo(WriteActivity):
    """Write Strava Activity to BigQuery"""

    def __init__(self, client: BigQueryClientWrapper):
        self._client = client
        self._dataset_name = "strava"
        self._table_name = "activities"

    def write_activity(self, activity: StravaActivity) -> None:
        activity_dict = [json.loads(activity.model_dump_json())]
        self._client.insert_rows_json(
            activity_dict, dataset_name=self._dataset_name, table_name=self._table_name
        )

    def create_activity_table(self) -> None:
        table_id = f"{self._client.project_id}.{self._dataset_name}.{self._table_name}"

        # MetaActivity model
        # https://developers.strava.com/docs/reference/#api-models-MetaActivity
        meta_activity_fields = [
            SchemaField("id", "INTEGER", mode="REQUIRED"),
            SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
        ]
        # MetaAthlete model
        # https://developers.strava.com/docs/reference/#api-models-MetaAthlete
        meta_athlete_fields = [
            SchemaField("id", "INTEGER", mode="REQUIRED"),
            SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
        ]
        # SummarySegment model
        # https://developers.strava.com/docs/reference/#api-models-SummarySegment
        summary_segment_fields = [
            SchemaField("id", "INTEGER", mode="REQUIRED"),
            SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("activity_type", "STRING", mode="REQUIRED"),
            SchemaField("distance", "FLOAT", mode="REQUIRED"),
            SchemaField("average_grade", "FLOAT", mode="REQUIRED"),
            SchemaField("maximum_grade", "FLOAT", mode="REQUIRED"),
            SchemaField("elevation_high", "FLOAT", mode="REQUIRED"),
            SchemaField("elevation_low", "FLOAT", mode="REQUIRED"),
            SchemaField("start_latlng", "FLOAT", mode="REPEATED"),
            SchemaField("end_latlng", "FLOAT", mode="REPEATED"),
            SchemaField("climb_category", "INTEGER", mode="REQUIRED"),
            SchemaField("city", "STRING", mode="NULLABLE"),
            SchemaField("state", "STRING", mode="NULLABLE"),
            SchemaField("country", "STRING", mode="NULLABLE"),
            SchemaField("private", "BOOLEAN", mode="REQUIRED"),
            SchemaField("hazardous", "BOOLEAN", mode="REQUIRED"),
            SchemaField("starred", "BOOLEAN", mode="REQUIRED"),
        ]

        # DetailedSegmentEffort model
        # https://developers.strava.com/docs/reference/#api-models-DetailedSegmentEffort
        detailed_segment_effort_fields = [
            SchemaField("id", "INTEGER", mode="REQUIRED"),
            SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField(
                "activity", "RECORD", mode="REQUIRED", fields=meta_activity_fields
            ),
            SchemaField(
                "athlete", "RECORD", mode="REQUIRED", fields=meta_athlete_fields
            ),
            SchemaField("elapsed_time", "INTEGER", mode="REQUIRED"),
            SchemaField("moving_time", "INTEGER", mode="REQUIRED"),
            SchemaField("start_date", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("start_date_local", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("distance", "FLOAT", mode="REQUIRED"),
            SchemaField("start_index", "INTEGER", mode="REQUIRED"),
            SchemaField("end_index", "INTEGER", mode="REQUIRED"),
            SchemaField("average_cadence", "FLOAT", mode="NULLABLE"),
            SchemaField("device_watts", "BOOLEAN", mode="NULLABLE"),
            SchemaField("average_watts", "FLOAT", mode="NULLABLE"),
            SchemaField(
                "segment", "RECORD", mode="REQUIRED", fields=summary_segment_fields
            ),
            SchemaField("kom_rank", "INTEGER", mode="NULLABLE"),
            SchemaField("pr_rank", "INTEGER", mode="NULLABLE"),
            SchemaField("hidden", "BOOLEAN", mode="REQUIRED"),
        ]

        # Split model
        # https://developers.strava.com/docs/reference/#api-models-Split
        split_fields = [
            SchemaField("distance", "FLOAT", mode="REQUIRED"),
            SchemaField("elapsed_time", "INTEGER", mode="REQUIRED"),
            SchemaField("elevation_difference", "FLOAT", mode="NULLABLE"),
            SchemaField("moving_time", "INTEGER", mode="REQUIRED"),
            SchemaField("split", "INTEGER", mode="REQUIRED"),
            SchemaField("average_speed", "FLOAT", mode="REQUIRED"),
            SchemaField("pace_zone", "INTEGER", mode="REQUIRED"),
        ]

        # Lap model
        # https://developers.strava.com/docs/reference/#api-models-Lap
        lap_fields = [
            SchemaField("id", "INTEGER", mode="REQUIRED"),
            SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField(
                "activity", "RECORD", mode="REQUIRED", fields=meta_activity_fields
            ),
            SchemaField(
                "athlete", "RECORD", mode="REQUIRED", fields=meta_athlete_fields
            ),
            SchemaField("elapsed_time", "INTEGER", mode="REQUIRED"),
            SchemaField("moving_time", "INTEGER", mode="REQUIRED"),
            SchemaField("start_date", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("start_date_local", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("distance", "FLOAT", mode="REQUIRED"),
            SchemaField("start_index", "INTEGER", mode="REQUIRED"),
            SchemaField("end_index", "INTEGER", mode="REQUIRED"),
            SchemaField("total_elevation_gain", "FLOAT", mode="NULLABLE"),
            SchemaField("average_speed", "FLOAT", mode="REQUIRED"),
            SchemaField("max_speed", "FLOAT", mode="REQUIRED"),
            SchemaField("average_cadence", "FLOAT", mode="NULLABLE"),
            SchemaField("device_watts", "BOOLEAN", mode="NULLABLE"),
            SchemaField("average_watts", "FLOAT", mode="NULLABLE"),
            SchemaField("lap_index", "INTEGER", mode="REQUIRED"),
            SchemaField("split", "INTEGER", mode="REQUIRED"),
        ]

        # DetailedActivity model + undocumented (new?) fields
        # https://developers.strava.com/docs/reference/#api-models-DetailedActivity
        schema = [
            SchemaField("id", "INTEGER", mode="REQUIRED"),
            SchemaField("external_id", "STRING", mode="NULLABLE"),
            SchemaField("upload_id", "INTEGER", mode="NULLABLE"),
            SchemaField(
                "athlete",
                "RECORD",
                mode="REQUIRED",
                fields=meta_athlete_fields,
            ),
            SchemaField("name", "STRING", mode="REQUIRED"),
            SchemaField("distance", "FLOAT", mode="REQUIRED"),
            SchemaField("moving_time", "INTEGER", mode="REQUIRED"),
            SchemaField("elapsed_time", "INTEGER", mode="REQUIRED"),
            SchemaField("total_elevation_gain", "FLOAT", mode="REQUIRED"),
            SchemaField("elev_high", "FLOAT", mode="NULLABLE"),
            SchemaField("elev_low", "FLOAT", mode="NULLABLE"),
            SchemaField("type", "STRING", mode="REQUIRED"),
            SchemaField("sport_type", "STRING", mode="REQUIRED"),
            SchemaField("start_date", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("start_date_local", "TIMESTAMP", mode="REQUIRED"),
            SchemaField("timezone", "STRING", mode="REQUIRED"),
            SchemaField("start_latlng", "FLOAT", mode="REPEATED"),
            SchemaField("end_latlng", "FLOAT", mode="REPEATED"),
            SchemaField("achievement_count", "INTEGER", mode="REQUIRED"),
            SchemaField("kudos_count", "INTEGER", mode="REQUIRED"),
            SchemaField("comment_count", "INTEGER", mode="REQUIRED"),
            SchemaField("athlete_count", "INTEGER", mode="REQUIRED"),
            SchemaField("photo_count", "INTEGER", mode="REQUIRED"),
            SchemaField("total_photo_count", "INTEGER", mode="REQUIRED"),
            SchemaField(
                "map",
                "RECORD",
                mode="REQUIRED",
                fields=[
                    SchemaField("id", "STRING", mode="REQUIRED"),
                    SchemaField("polyline", "STRING", mode="REQUIRED"),
                    SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
                    SchemaField("summary_polyline", "STRING", mode="REQUIRED"),
                ],
            ),
            SchemaField("trainer", "BOOLEAN", mode="REQUIRED"),
            SchemaField("commute", "BOOLEAN", mode="REQUIRED"),
            SchemaField("manual", "BOOLEAN", mode="REQUIRED"),
            SchemaField("private", "BOOLEAN", mode="REQUIRED"),
            SchemaField("flagged", "BOOLEAN", mode="REQUIRED"),
            SchemaField("workout_type", "STRING", mode="NULLABLE"),
            SchemaField("upload_id_str", "STRING", mode="NULLABLE"),
            SchemaField("average_speed", "FLOAT", mode="REQUIRED"),
            SchemaField("max_speed", "FLOAT", mode="REQUIRED"),
            SchemaField("has_kudoed", "BOOLEAN", mode="REQUIRED"),
            SchemaField("hide_from_home", "BOOLEAN", mode="REQUIRED"),
            SchemaField("gear_id", "STRING", mode="NULLABLE"),
            SchemaField("kilojoules", "FLOAT", mode="NULLABLE"),
            SchemaField("average_watts", "FLOAT", mode="NULLABLE"),
            SchemaField("device_watts", "BOOLEAN", mode="NULLABLE"),
            SchemaField("max_watts", "INTEGER", mode="NULLABLE"),
            SchemaField("weighted_average_watts", "INTEGER", mode="NULLABLE"),
            SchemaField("description", "STRING", mode="NULLABLE"),
            SchemaField(
                "photos",
                "RECORD",
                mode="REQUIRED",
                fields=[
                    SchemaField(
                        "primary",
                        "RECORD",
                        mode="NULLABLE",
                        fields=[
                            SchemaField("id", "STRING", mode="NULLABLE"),
                            SchemaField("media_type", "INTEGER", mode="NULLABLE"),
                            SchemaField("source", "INTEGER", mode="REQUIRED"),
                            SchemaField("unique_id", "STRING", mode="REQUIRED"),
                            SchemaField("urls", "JSON", mode="REQUIRED"),
                        ],
                    ),
                    SchemaField("count", "INTEGER", mode="REQUIRED"),
                ],
            ),
            SchemaField(
                "gear",
                "RECORD",
                mode="NULLABLE",
                fields=[
                    SchemaField("id", "STRING", mode="REQUIRED"),
                    SchemaField("primary", "BOOLEAN", mode="REQUIRED"),
                    SchemaField("name", "STRING", mode="REQUIRED"),
                    SchemaField("resource_state", "INTEGER", mode="REQUIRED"),
                    SchemaField("distance", "FLOAT", mode="REQUIRED"),
                ],
            ),
            SchemaField("calories", "FLOAT", mode="REQUIRED"),
            SchemaField(
                "segment_efforts",
                "RECORD",
                mode="REPEATED",
                fields=detailed_segment_effort_fields,
            ),
            SchemaField("device_name", "STRING", mode="NULLABLE"),
            SchemaField("embed_token", "STRING", mode="REQUIRED"),
            SchemaField(
                "splits_metric", "RECORD", mode="REPEATED", fields=split_fields
            ),
            SchemaField(
                "splits_standard", "RECORD", mode="REPEATED", fields=split_fields
            ),
            SchemaField("laps", "RECORD", mode="REPEATED", fields=lap_fields),
            SchemaField(
                "best_efforts",
                "RECORD",
                mode="REPEATED",
                fields=detailed_segment_effort_fields,
            ),
            # Not in DetailedActivity model
            SchemaField("average_cadence", "FLOAT", mode="NULLABLE"),
            SchemaField("has_heartrate", "BOOLEAN", mode="REQUIRED"),
            SchemaField("pr_count", "INTEGER", mode="REQUIRED"),
            SchemaField("suffer_score", "FLOAT", mode="NULLABLE"),
            SchemaField(
                "stats_visibility",
                "RECORD",
                mode="REPEATED",
                fields=[
                    SchemaField("type", "STRING", mode="REQUIRED"),
                    SchemaField("visibility", "STRING", mode="REQUIRED"),
                ],
            ),
            SchemaField("display_hide_heartrate_option", "BOOLEAN", mode="NULLABLE"),
            SchemaField("heartrate_opt_out", "BOOLEAN", mode="NULLABLE"),
            SchemaField("average_heartrate", "FLOAT", mode="NULLABLE"),
            SchemaField("max_heartrate", "FLOAT", mode="NULLABLE"),
            SchemaField("available_zones", "STRING", mode="REPEATED"),
            SchemaField("visibility", "STRING", mode="NULLABLE"),
        ]
        self._client.create_table(table_id, schema=schema)
