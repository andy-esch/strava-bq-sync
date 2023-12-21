import logging
from google.cloud.bigquery import Client, SchemaField, Table

logger = logging.getLogger(__name__)


class BigQueryClientWrapper:
    def __init__(self, *, project_id: str):
        self.project_id = project_id
        self._client = Client(project=project_id)

    def insert_rows_json(
        self, rows: list[dict], *, dataset_name: str, table_name: str
    ) -> None:
        """Insert each dict in rows as a new row in `dataset.table_name`
        https://cloud.google.com/bigquery/docs/samples/bigquery-table-insert-rows#bigquery_table_insert_rows-python
        """
        table_id = f"{self.project_id}.{dataset_name}.{table_name}"
        errors = self._client.insert_rows_json(table_id, rows)
        if len(errors) > 0:
            raise Exception("Errors: %s", errors)
        logger.info("Successfully inserted %s rows into %s.", len(rows), table_id)

    def create_table(self, table_id: str, *, schema: list[SchemaField]):
        table = Table(table_id, schema=schema)
        table = self._client.create_table(table)
