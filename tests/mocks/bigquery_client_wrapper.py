from google.cloud.bigquery import SchemaField

from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper


class MockBigQueryClientWrapper(BigQueryClientWrapper):
    def __init__(self, *, project_id: str):
        self.project_id = project_id
        self.table_name = None
        self.dataset_name = None
        self.written_activities = None
        self.table_id = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Mock doesn't need cleanup

    def close(self):
        pass  # Mock doesn't need cleanup

    def insert_rows_json(
        self, rows: list[dict], *, dataset_name: str, table_name: str
    ) -> None:
        self.written_activities = rows
        self.table_name = table_name
        self.dataset_name = dataset_name

    def create_table(self, table_id: str, *, schema: list[SchemaField]):
        self.table_id = table_id
        self.schema = schema
