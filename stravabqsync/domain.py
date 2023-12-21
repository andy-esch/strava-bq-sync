from datetime import datetime
from typing import NamedTuple

from pydantic import BaseModel, Field


class WebhookRequest(BaseModel):
    aspect_type: str
    event_time: int
    object_id: int
    object_type: str
    owner_id: int
    subscription_id: int
    updates: dict


class MetaAthlete(BaseModel):
    id: int
    resource_state: int


class PolylineMap(BaseModel):
    id: str
    polyline: str
    resource_state: int
    summary_polyline: str


class MetaActivity(BaseModel):
    id: int
    resource_state: int


class SummarySegment(BaseModel):
    id: int
    resource_state: int
    name: str
    activity_type: str
    distance: float
    average_grade: float
    maximum_grade: float
    elevation_high: float
    elevation_low: float
    start_latlng: list[float]
    end_latlng: list[float]
    climb_category: int
    city: str | None = None
    state: str | None = None
    country: str | None = None
    private: bool
    hazardous: bool
    starred: bool


class DetailedSegmentEffort(BaseModel):
    id: int
    resource_state: int
    name: str
    activity: MetaActivity
    athlete: MetaAthlete
    elapsed_time: int
    moving_time: int
    start_date: datetime
    start_date_local: datetime
    distance: float
    start_index: int
    end_index: int
    average_cadence: float | None = None
    device_watts: bool | None = None
    average_watts: float | None = None
    segment: SummarySegment
    kom_rank: int | None
    pr_rank: int | None
    hidden: bool


class Split(BaseModel):
    distance: float
    elapsed_time: int
    elevation_difference: float | None = None
    moving_time: int
    split: int
    average_speed: float
    pace_zone: int


class Lap(BaseModel):
    id: int
    resource_state: int
    name: str
    activity: MetaActivity
    athlete: MetaAthlete
    elapsed_time: int
    moving_time: int
    start_date: datetime
    start_date_local: datetime
    distance: float
    start_index: int
    end_index: int
    total_elevation_gain: float | None = None
    average_speed: float
    max_speed: float
    average_cadence: float | None = None
    device_watts: bool | None = None
    average_watts: float | None = None
    lap_index: int
    split: int


class SummaryGear(BaseModel):
    id: str
    primary: bool
    name: str
    resource_state: int
    distance: float


class PhotosSummary_primary(BaseModel):
    id: str | None = None
    media_type: int | None = None
    source: int
    unique_id: str
    urls: dict[str, str]


class PhotosSummary(BaseModel):
    primary: PhotosSummary_primary | None = None
    count: int


class StatsVisibility(BaseModel):
    type: str
    visibility: str


class StravaActivity(BaseModel):
    id: int
    external_id: str | None = None
    upload_id: int | None = None
    athlete: MetaAthlete
    name: str
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    elev_high: float | None = None
    elev_low: float | None = None
    type: str
    sport_type: str
    start_date: datetime
    start_date_local: datetime
    timezone: str
    start_latlng: list[float]
    end_latlng: list[float]
    achievement_count: int
    kudos_count: int
    comment_count: int
    athlete_count: int
    photo_count: int
    total_photo_count: int
    map: PolylineMap
    trainer: bool
    commute: bool
    manual: bool
    private: bool
    flagged: bool
    workout_type: int | None = None
    upload_id_str: str | None = None
    average_speed: float
    max_speed: float
    has_kudoed: bool
    hide_from_home: bool
    gear_id: str | None = None
    kilojoules: float | None = None
    average_watts: float | None = None
    device_watts: bool | None = None
    max_watts: int | None = None
    weighted_average_watts: int | None = None
    description: str | None = None
    photos: PhotosSummary
    gear: SummaryGear | None = None
    calories: float
    segment_efforts: list[DetailedSegmentEffort]
    device_name: str | None = None
    embed_token: str
    splits_metric: list[Split] = Field(default_factory=list)
    splits_standard: list[Split] = Field(default_factory=list)
    laps: list[Lap] = Field(default_factory=list)
    best_efforts: list[DetailedSegmentEffort] = Field(default_factory=list)

    # Not in DetailedActivity model
    average_cadence: float | None = None
    has_heartrate: bool
    pr_count: int
    suffer_score: float | None = None
    stats_visibility: list[StatsVisibility] = Field(default_factory=list)
    display_hide_heartrate_option: bool | None = None
    heartrate_opt_out: bool | None = None
    average_heartrate: float | None = None
    max_heartrate: float | None = None
    available_zones: list[str] = Field(default_factory=list)
    visibility: str | None = None


class StravaTokenSet(NamedTuple):
    client_id: int
    client_secret: str
    access_token: str
    refresh_token: str


class GitHubTokenSet(NamedTuple):
    github: str
