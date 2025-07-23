import json
import os
import tempfile
from unittest.mock import patch

import pytest

from stravabqsync.config import (
    AppConfig,
    StravaApiConfig,
    _get_required_env_var,
    load_config,
)
from stravabqsync.exceptions import ConfigurationError


class TestGetRequiredEnvVar:
    def test_get_required_env_var_success(self):
        config = {"TEST_KEY": "test_value"}
        result = _get_required_env_var(config, "TEST_KEY")
        assert result == "test_value"

    def test_get_required_env_var_missing_raises_error(self):
        # This test covers line 19: raise ConfigurationError
        config = {"OTHER_KEY": "value"}
        with pytest.raises(ConfigurationError) as exc_info:
            _get_required_env_var(config, "MISSING_KEY")
        assert "MISSING_KEY environment variable is required" in str(exc_info.value)

    def test_get_required_env_var_none_value_raises_error(self):
        config = {"TEST_KEY": None}
        with pytest.raises(ConfigurationError) as exc_info:
            _get_required_env_var(config, "TEST_KEY")
        assert "TEST_KEY environment variable is required" in str(exc_info.value)


class TestStravaApiConfig:
    def test_strava_api_config_defaults(self):
        config = StravaApiConfig()
        assert config.token_url == "https://www.strava.com/oauth/token"
        assert config.api_base_url == "https://www.strava.com/api/v3"
        assert config.request_timeout == 10
        assert config.token_retry_attempts == 2
        assert config.token_retry_backoff == 0.5
        assert config.activity_retry_attempts == 3
        assert config.activity_retry_backoff == 1.0


class TestLoadConfig:
    @patch("stravabqsync.config.dotenv_values")
    @patch.dict(
        os.environ,
        {
            "STRAVA_CLIENT_ID": "123",
            "STRAVA_CLIENT_SECRET": "secret",
            "STRAVA_REFRESH_TOKEN": "refresh",
            "GCP_PROJECT_ID": "project",
            "GCP_BIGQUERY_DATASET": "dataset",
        },
        clear=True,
    )
    def test_load_config_success(self, mock_dotenv_values):
        mock_dotenv_values.return_value = {}
        config = load_config()
        assert isinstance(config, AppConfig)
        assert config.tokens.client_id == 123
        assert config.tokens.client_secret == "secret"
        assert config.tokens.refresh_token == "refresh"
        assert config.tokens.access_token == ""
        assert config.project_id == "project"
        assert config.bq_dataset == "dataset"
        assert isinstance(config.strava_api, StravaApiConfig)

    @patch("stravabqsync.config.dotenv_values")
    @patch.dict(os.environ, {}, clear=True)
    def test_load_config_missing_env_var(self, mock_dotenv_values):
        mock_dotenv_values.return_value = {}
        with pytest.raises(ConfigurationError):
            load_config()

    @patch("stravabqsync.config.dotenv_values")
    @patch.dict(
        os.environ,
        {
            "STRAVA_CLIENT_ID": "123",
            "STRAVA_CLIENT_SECRET": "secret",
            "STRAVA_REFRESH_TOKEN": "refresh",
            "GCP_PROJECT_ID": "project",
            "GCP_BIGQUERY_DATASET": "dataset",
        },
        clear=True,
    )
    def test_load_config_with_secrets_file(self, mock_dotenv_values):
        # This test covers lines 71-72: secrets file loading
        mock_dotenv_values.return_value = {}
        secrets_data = {
            "STRAVA_CLIENT_ID": "456",  # Should override env var
            "STRAVA_CLIENT_SECRET": "file_secret",
        }

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as temp_file:
            json.dump(secrets_data, temp_file)
            temp_file.flush()

            try:
                with patch.dict(
                    os.environ, {"STRAVA_SECRETS_PATH": temp_file.name}, clear=False
                ):
                    config = load_config()
                    # Secrets file should override environment variables
                    assert config.tokens.client_id == 456
                    assert config.tokens.client_secret == "file_secret"
            finally:
                os.unlink(temp_file.name)

    @patch("stravabqsync.config.dotenv_values")
    @patch.dict(
        os.environ,
        {
            "STRAVA_CLIENT_ID": "123",
            "STRAVA_CLIENT_SECRET": "secret",
            "STRAVA_REFRESH_TOKEN": "refresh",
            "GCP_PROJECT_ID": "project",
            "GCP_BIGQUERY_DATASET": "dataset",
            "STRAVA_SECRETS_PATH": "/nonexistent/path.json",
        },
        clear=True,
    )
    def test_load_config_nonexistent_secrets_file(self, mock_dotenv_values):
        # Test that nonexistent secrets file doesn't break loading
        mock_dotenv_values.return_value = {}
        config = load_config()
        assert config.tokens.client_id == 123
        assert config.tokens.client_secret == "secret"
