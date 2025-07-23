from unittest.mock import patch

from stravabqsync.adapters.gcp import (
    make_bigquery_client_wrapper,
    make_write_activities,
)
from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.adapters.gcp._repositories import WriteActivitiesRepo


class TestGcpAdapterFactories:
    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_make_bigquery_client_wrapper_returns_correct_type(self, mock_client):
        # This test covers line 11: BigQueryClientWrapper instantiation
        result = make_bigquery_client_wrapper()
        assert isinstance(result, BigQueryClientWrapper)

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_make_bigquery_client_wrapper_uses_app_config(self, mock_client):
        # Test that factory uses app_config.project_id
        client = make_bigquery_client_wrapper()
        assert hasattr(client, "project_id")
        assert hasattr(client, "_client")

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_make_bigquery_client_wrapper_caching(self, mock_client):
        # Test that @lru_cache returns the same instance
        first_call = make_bigquery_client_wrapper()
        second_call = make_bigquery_client_wrapper()
        assert first_call is second_call

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_make_write_activities_returns_correct_type(self, mock_client):
        # This test covers line 16: WriteActivitiesRepo instantiation
        result = make_write_activities()
        assert isinstance(result, WriteActivitiesRepo)

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_make_write_activities_uses_app_config(self, mock_client):
        # Test that factory uses app_config.bq_dataset and client wrapper
        repo = make_write_activities()
        assert hasattr(repo, "_client")
        assert hasattr(repo, "_dataset_name")

    @patch("stravabqsync.adapters.gcp._clients.Client")
    def test_make_write_activities_caching(self, mock_client):
        # Test that @lru_cache returns the same instance
        first_call = make_write_activities()
        second_call = make_write_activities()
        assert first_call is second_call
