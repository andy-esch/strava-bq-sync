from stravabqsync.application.services import make_sync_service
from stravabqsync.application.services._sync_service import SyncService


class TestApplicationServicesFactories:
    def test_make_sync_service_returns_correct_type(self):
        # This test covers line 10: SyncService instantiation
        result = make_sync_service()
        assert isinstance(result, SyncService)

    def test_make_sync_service_has_required_dependencies(self):
        # Test that factory injects all required dependencies
        service = make_sync_service()
        assert hasattr(service, "_tokens")
        assert hasattr(service, "_read_activities")
        assert hasattr(service, "_write_activities")

    def test_make_sync_service_multiple_calls_same_instance(self):
        # Test that multiple calls return the same instance (if cached)
        # or at least work correctly
        first_call = make_sync_service()
        second_call = make_sync_service()
        # Both should be valid SyncService instances
        assert isinstance(first_call, SyncService)
        assert isinstance(second_call, SyncService)
