from unittest.mock import MagicMock, patch

import pytest
from google.cloud.bigquery import SchemaField, Table

from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.exceptions import BigQueryError


class TestBigQueryClientWrapper:
    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_init(self, mock_client_class):
        # This test covers lines 12-13: constructor
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        wrapper = BigQueryClientWrapper(project_id="test-project")

        assert wrapper.project_id == "test-project"
        assert wrapper._client == mock_client_instance
        mock_client_class.assert_called_once_with(project="test-project")

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_insert_rows_json_success(self, mock_client_class):
        # This test covers line 27: successful insertion logging
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance
        mock_client_instance.insert_rows_json.return_value = []  # No errors

        wrapper = BigQueryClientWrapper(project_id="test-project")
        test_rows = [{"id": 1, "name": "test"}, {"id": 2, "name": "test2"}]

        wrapper.insert_rows_json(
            test_rows, dataset_name="test_dataset", table_name="test_table"
        )

        expected_table_id = "test-project.test_dataset.test_table"
        mock_client_instance.insert_rows_json.assert_called_once_with(
            expected_table_id, test_rows
        )

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_insert_rows_json_with_errors(self, mock_client_class):
        # This test covers lines 21-26: error handling path
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        # Mock errors returned from BigQuery
        mock_errors = [{"error": "field_error"}, {"error": "type_error"}]
        mock_client_instance.insert_rows_json.return_value = mock_errors

        wrapper = BigQueryClientWrapper(project_id="test-project")
        test_rows = [{"id": 1, "name": "test"}]

        with pytest.raises(BigQueryError) as exc_info:
            wrapper.insert_rows_json(
                test_rows, dataset_name="test_dataset", table_name="test_table"
            )

        expected_table_id = "test-project.test_dataset.test_table"
        expected_message = f"Failed to insert 1 rows into {expected_table_id}"

        assert str(exc_info.value) == expected_message
        assert exc_info.value.errors == mock_errors
        mock_client_instance.insert_rows_json.assert_called_once_with(
            expected_table_id, test_rows
        )

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_create_table(self, mock_client_class):
        # This test covers lines 31-33: create_table method
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        # Mock the table creation
        mock_created_table = MagicMock(spec=Table)
        mock_client_instance.create_table.return_value = mock_created_table

        wrapper = BigQueryClientWrapper(project_id="test-project")
        test_schema = [
            SchemaField("id", "INTEGER"),
            SchemaField("name", "STRING"),
        ]
        table_id = "test-project.test_dataset.test_table"

        result = wrapper.create_table(table_id, schema=test_schema)

        assert result == mock_created_table

        # Verify create_table was called with a Table object
        mock_client_instance.create_table.assert_called_once()
        call_args = mock_client_instance.create_table.call_args[0]
        created_table_arg = call_args[0]

        assert isinstance(created_table_arg, Table)
        # The Table constructor parses the full table_id and extracts
        #  just the table name
        assert created_table_arg.table_id == "test_table"
        assert created_table_arg.schema == test_schema
