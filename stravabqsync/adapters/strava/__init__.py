from functools import lru_cache

from stravabqsync.adapters.strava._repositories import (
    StravaActivitiesRepo,
    StravaTokenRepo,
)
from stravabqsync.config import StravaTokenSet, app_config
from stravabqsync.ports.out.read import ReadActivities


@lru_cache
def make_read_strava_token():
    return StravaTokenRepo(app_config.tokens)


@lru_cache
def make_read_activities(strava_tokens: StravaTokenSet) -> ReadActivities:
    return StravaActivitiesRepo(strava_tokens)
