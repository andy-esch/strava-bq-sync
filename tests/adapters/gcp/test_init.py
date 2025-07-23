from stravabqsync.adapters.gcp import (
    make_bigquery_client_wrapper,
    make_write_activities,
)
from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.adapters.gcp._repositories import WriteActivitiesRepo


class TestGcpAdapterFactories:
    def test_make_bigquery_client_wrapper_returns_correct_type(self):
        # This test covers line 11: BigQueryClientWrapper instantiation
        result = make_bigquery_client_wrapper()
        assert isinstance(result, BigQueryClientWrapper)

    def test_make_bigquery_client_wrapper_uses_app_config(self):
        # Test that factory uses app_config.project_id
        client = make_bigquery_client_wrapper()
        assert hasattr(client, "project_id")
        assert hasattr(client, "_client")

    def test_make_bigquery_client_wrapper_caching(self):
        # Test that @lru_cache returns the same instance
        first_call = make_bigquery_client_wrapper()
        second_call = make_bigquery_client_wrapper()
        assert first_call is second_call

    def test_make_write_activities_returns_correct_type(self):
        # This test covers line 16: WriteActivitiesRepo instantiation
        result = make_write_activities()
        assert isinstance(result, WriteActivitiesRepo)

    def test_make_write_activities_uses_app_config(self):
        # Test that factory uses app_config.bq_dataset and client wrapper
        repo = make_write_activities()
        assert hasattr(repo, "_client")
        assert hasattr(repo, "_dataset_name")

    def test_make_write_activities_caching(self):
        # Test that @lru_cache returns the same instance
        first_call = make_write_activities()
        second_call = make_write_activities()
        assert first_call is second_call
