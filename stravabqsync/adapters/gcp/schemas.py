"""BigQuery schema definitions for Strava data models."""

from google.cloud.bigquery import SchemaField

# Type and mode constants
INTEGER = "INTEGER"
STRING = "STRING"
FLOAT = "FLOAT"
BOOLEAN = "BOOLEAN"
TIMESTAMP = "TIMESTAMP"
JSON = "JSON"
RECORD = "RECORD"

REQUIRED = "REQUIRED"
NULLABLE = "NULLABLE"
REPEATED = "REPEATED"

# Helper functions for common field patterns


def required_int(name: str) -> SchemaField:
    """Create a required integer field."""
    return SchemaField(name, INTEGER, mode=REQUIRED)


def required_string(name: str) -> SchemaField:
    """Create a required string field."""
    return SchemaField(name, STRING, mode=REQUIRED)


def required_float(name: str) -> SchemaField:
    """Create a required float field."""
    return SchemaField(name, FLOAT, mode=REQUIRED)


def required_bool(name: str) -> SchemaField:
    """Create a required boolean field."""
    return SchemaField(name, BOOLEAN, mode=REQUIRED)


def required_timestamp(name: str) -> SchemaField:
    """Create a required timestamp field."""
    return SchemaField(name, TIMESTAMP, mode=REQUIRED)


def nullable_string(name: str) -> SchemaField:
    """Create a nullable string field."""
    return SchemaField(name, STRING, mode=NULLABLE)


def nullable_float(name: str) -> SchemaField:
    """Create a nullable float field."""
    return SchemaField(name, FLOAT, mode=NULLABLE)


def nullable_int(name: str) -> SchemaField:
    """Create a nullable integer field."""
    return SchemaField(name, INTEGER, mode=NULLABLE)


def nullable_bool(name: str) -> SchemaField:
    """Create a nullable boolean field."""
    return SchemaField(name, BOOLEAN, mode=NULLABLE)


def repeated_float(name: str) -> SchemaField:
    """Create a repeated float field."""
    return SchemaField(name, FLOAT, mode=REPEATED)


def repeated_string(name: str) -> SchemaField:
    """Create a repeated string field."""
    return SchemaField(name, STRING, mode=REPEATED)


# MetaActivity model
# https://developers.strava.com/docs/reference/#api-models-MetaActivity
META_ACTIVITY_FIELDS = [
    required_int("id"),
    required_int("resource_state"),
]

# MetaAthlete model
# https://developers.strava.com/docs/reference/#api-models-MetaAthlete
META_ATHLETE_FIELDS = [
    required_int("id"),
    required_int("resource_state"),
]

# SummarySegment model
# https://developers.strava.com/docs/reference/#api-models-SummarySegment
SUMMARY_SEGMENT_FIELDS = [
    required_int("id"),
    required_int("resource_state"),
    required_string("name"),
    required_string("activity_type"),
    required_float("distance"),
    required_float("average_grade"),
    required_float("maximum_grade"),
    required_float("elevation_high"),
    required_float("elevation_low"),
    repeated_float("start_latlng"),
    repeated_float("end_latlng"),
    required_int("climb_category"),
    nullable_string("city"),
    nullable_string("state"),
    nullable_string("country"),
    required_bool("private"),
    required_bool("hazardous"),
    required_bool("starred"),
]

# DetailedSegmentEffort model
# https://developers.strava.com/docs/reference/#api-models-DetailedSegmentEffort
DETAILED_SEGMENT_EFFORT_FIELDS = [
    required_int("id"),
    required_int("resource_state"),
    required_string("name"),
    SchemaField("activity", RECORD, mode=REQUIRED, fields=META_ACTIVITY_FIELDS),
    SchemaField("athlete", RECORD, mode=REQUIRED, fields=META_ATHLETE_FIELDS),
    required_int("elapsed_time"),
    required_int("moving_time"),
    required_timestamp("start_date"),
    required_timestamp("start_date_local"),
    required_float("distance"),
    required_int("start_index"),
    required_int("end_index"),
    nullable_float("average_cadence"),
    nullable_bool("device_watts"),
    nullable_float("average_watts"),
    SchemaField("segment", RECORD, mode=NULLABLE, fields=SUMMARY_SEGMENT_FIELDS),
    nullable_int("kom_rank"),
    nullable_int("pr_rank"),
    nullable_bool("hidden"),
]

# Split model
# https://developers.strava.com/docs/reference/#api-models-Split
SPLIT_FIELDS = [
    required_float("distance"),
    required_int("elapsed_time"),
    nullable_float("elevation_difference"),
    required_int("moving_time"),
    required_int("split"),
    required_float("average_speed"),
    required_int("pace_zone"),
]

# Lap model
# https://developers.strava.com/docs/reference/#api-models-Lap
LAP_FIELDS = [
    required_int("id"),
    required_int("resource_state"),
    required_string("name"),
    SchemaField("activity", RECORD, mode=REQUIRED, fields=META_ACTIVITY_FIELDS),
    SchemaField("athlete", RECORD, mode=REQUIRED, fields=META_ATHLETE_FIELDS),
    required_int("elapsed_time"),
    required_int("moving_time"),
    required_timestamp("start_date"),
    required_timestamp("start_date_local"),
    required_float("distance"),
    required_int("start_index"),
    required_int("end_index"),
    nullable_float("total_elevation_gain"),
    required_float("average_speed"),
    required_float("max_speed"),
    nullable_float("average_cadence"),
    nullable_bool("device_watts"),
    nullable_float("average_watts"),
    required_int("lap_index"),
    required_int("split"),
]

# PolylineMap fields
POLYLINE_MAP_FIELDS = [
    required_string("id"),
    required_string("polyline"),
    required_int("resource_state"),
    required_string("summary_polyline"),
]

# PhotosSummary fields
PHOTOS_SUMMARY_FIELDS = [
    SchemaField(
        "primary",
        RECORD,
        mode=NULLABLE,
        fields=[
            nullable_string("id"),
            nullable_int("media_type"),
            required_int("source"),
            required_string("unique_id"),
            SchemaField("urls", JSON, mode=REQUIRED),
        ],
    ),
    required_int("count"),
]

# SummaryGear fields
SUMMARY_GEAR_FIELDS = [
    required_string("id"),
    required_bool("primary"),
    required_string("name"),
    required_int("resource_state"),
    required_float("distance"),
]

# StatsVisibility fields
STATS_VISIBILITY_FIELDS = [
    required_string("type"),
    required_string("visibility"),
]

# Main Strava Activity schema (DetailedActivity model + undocumented fields)
# https://developers.strava.com/docs/reference/#api-models-DetailedActivity
STRAVA_ACTIVITY_SCHEMA = [
    required_int("id"),
    nullable_string("external_id"),
    nullable_int("upload_id"),
    SchemaField("athlete", RECORD, mode=REQUIRED, fields=META_ATHLETE_FIELDS),
    required_string("name"),
    required_float("distance"),
    required_int("moving_time"),
    required_int("elapsed_time"),
    required_float("total_elevation_gain"),
    nullable_float("elev_high"),
    nullable_float("elev_low"),
    required_string("type"),
    required_string("sport_type"),
    required_timestamp("start_date"),
    required_timestamp("start_date_local"),
    required_string("timezone"),
    repeated_float("start_latlng"),
    repeated_float("end_latlng"),
    required_int("achievement_count"),
    required_int("kudos_count"),
    required_int("comment_count"),
    required_int("athlete_count"),
    required_int("photo_count"),
    required_int("total_photo_count"),
    SchemaField("map", RECORD, mode=REQUIRED, fields=POLYLINE_MAP_FIELDS),
    required_bool("trainer"),
    required_bool("commute"),
    required_bool("manual"),
    required_bool("private"),
    required_bool("flagged"),
    nullable_string("workout_type"),
    nullable_string("upload_id_str"),
    required_float("average_speed"),
    required_float("max_speed"),
    required_bool("has_kudoed"),
    required_bool("hide_from_home"),
    nullable_string("gear_id"),
    nullable_float("kilojoules"),
    nullable_float("average_watts"),
    nullable_bool("device_watts"),
    nullable_int("max_watts"),
    nullable_int("weighted_average_watts"),
    nullable_string("description"),
    SchemaField("photos", RECORD, mode=REQUIRED, fields=PHOTOS_SUMMARY_FIELDS),
    SchemaField("gear", RECORD, mode=NULLABLE, fields=SUMMARY_GEAR_FIELDS),
    required_float("calories"),
    SchemaField(
        "segment_efforts",
        RECORD,
        mode=REPEATED,
        fields=DETAILED_SEGMENT_EFFORT_FIELDS,
    ),
    nullable_string("device_name"),
    required_string("embed_token"),
    SchemaField("splits_metric", RECORD, mode=REPEATED, fields=SPLIT_FIELDS),
    SchemaField("splits_standard", RECORD, mode=REPEATED, fields=SPLIT_FIELDS),
    SchemaField("laps", RECORD, mode=REPEATED, fields=LAP_FIELDS),
    SchemaField(
        "best_efforts", RECORD, mode=REPEATED, fields=DETAILED_SEGMENT_EFFORT_FIELDS
    ),
    # Not in DetailedActivity model
    nullable_float("average_cadence"),
    required_bool("has_heartrate"),
    required_int("pr_count"),
    nullable_float("suffer_score"),
    SchemaField(
        "stats_visibility", RECORD, mode=REPEATED, fields=STATS_VISIBILITY_FIELDS
    ),
    nullable_bool("display_hide_heartrate_option"),
    nullable_bool("heartrate_opt_out"),
    nullable_float("average_heartrate"),
    nullable_float("max_heartrate"),
    repeated_string("available_zones"),
    nullable_string("visibility"),
]
