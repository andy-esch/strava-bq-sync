from stravabqsync.adapters import Supplier
from stravabqsync.ports.out.read import ReadActivity
from stravabqsync.ports.out.write import WriteActivity


class SyncService:
    """Receive Webhook message, parse and fetch related activity, and write
    activity to BigQuery"""

    def __init__(
        self,
        read_activity: Supplier[ReadActivity],
        write_activity: Supplier[WriteActivity],
    ):
        self._read_activity = read_activity
        self._write_activity = write_activity

    def run(self, activity_id: int) -> None:
        activity = self._read_activity().read_activity_by_id(activity_id)
        self._write_activity().write_activity(activity)
