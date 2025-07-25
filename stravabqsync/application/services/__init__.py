from functools import lru_cache

from stravabqsync.adapters.gcp import make_write_activities
from stravabqsync.adapters.strava import make_read_activities, make_read_strava_token
from stravabqsync.application.services._sync_service import SyncService


@lru_cache(maxsize=1)
def make_sync_service() -> SyncService:
    """Create a configured SyncService instance.

    Factory function that wires together all dependencies needed for the
    sync service. Uses LRU cache to ensure singleton behavior.

    Returns:
        SyncService: Fully configured sync service instance.

    Raises:
        StravaTokenError: If initial token refresh fails.
        ConfigurationError: If required configuration is missing.
    """
    return SyncService(
        read_strava_token=make_read_strava_token,
        read_activities=make_read_activities,
        write_activities=make_write_activities,
    )
