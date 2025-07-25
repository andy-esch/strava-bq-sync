from typing import Callable

from stravabqsync.adapters import Supplier
from stravabqsync.domain import StravaTokenSet
from stravabqsync.ports.out.read import ReadActivities, ReadStravaToken
from stravabqsync.ports.out.write import WriteActivities


class SyncService:
    """Receive Webhook message, parse and fetch related activity, and write
    activity to BigQuery"""

    def __init__(
        self,
        read_strava_token: Supplier[ReadStravaToken],
        read_activities: Callable[[StravaTokenSet], ReadActivities],
        write_activities: Supplier[WriteActivities],
    ):
        """Initialize the sync service with required dependencies.

        Args:
            read_strava_token: Factory function for token refresh service.
            read_activities: Factory function for activity reading service.
            write_activities: Factory function for activity writing service.

        Raises:
            StravaTokenError: If initial token refresh fails.
            StravaApiError: If token refresh API call fails.
        """
        self._tokens = read_strava_token().refresh()
        self._read_activities = read_activities(self._tokens)
        self._write_activities = write_activities()

    def run(self, activity_id: int) -> None:
        """Sync data for `activity_id` from Strava to BigQuery activities table"""
        activity = self._read_activities.read_activity_by_id(activity_id)
        self._write_activities.write_activity(activity)
