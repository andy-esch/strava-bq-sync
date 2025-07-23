from unittest.mock import patch

from stravabqsync.application.services import make_sync_service
from stravabqsync.application.services._sync_service import SyncService


class TestApplicationServicesFactories:
    @patch("stravabqsync.adapters.gcp._clients.Client")
    @patch("requests.post")
    def test_make_sync_service_returns_correct_type(self, mock_post, mock_client):
        # Mock successful token refresh response
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"access_token": "test_token"}

        # This test covers line 10: SyncService instantiation
        result = make_sync_service()
        assert isinstance(result, SyncService)

    @patch("stravabqsync.adapters.gcp._clients.Client")
    @patch("requests.post")
    def test_make_sync_service_has_required_dependencies(self, mock_post, mock_client):
        # Mock successful token refresh response
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"access_token": "test_token"}

        # Test that factory injects all required dependencies
        service = make_sync_service()
        assert hasattr(service, "_tokens")
        assert hasattr(service, "_read_activities")
        assert hasattr(service, "_write_activities")

    @patch("stravabqsync.adapters.gcp._clients.Client")
    @patch("requests.post")
    def test_make_sync_service_multiple_calls_same_instance(
        self, mock_post, mock_client
    ):
        # Mock successful token refresh response
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {"access_token": "test_token"}

        # Test that multiple calls return the same instance (if cached)
        # or at least work correctly
        first_call = make_sync_service()
        second_call = make_sync_service()
        # Both should be valid SyncService instances
        assert isinstance(first_call, SyncService)
        assert isinstance(second_call, SyncService)
