"""Token loader"""

import json
import os
from typing import NamedTuple

from dotenv import dotenv_values

from stravabqsync.exceptions import ConfigurationError


def _get_required_env_var(config: dict[str, str | None], key: str) -> str:
    """Get required environment variable or raise ConfigurationError with helpful
    message.
    """
    value = config.get(key)
    if value is None:
        raise ConfigurationError(f"{key} environment variable is required")
    return value


class StravaTokenSet(NamedTuple):
    """OAuth token set for Strava"""

    client_id: int
    client_secret: str
    refresh_token: str
    access_token: str | None = None


class AppConfig(NamedTuple):
    """Strava-bq-sync application configuration

    Attributes:
      tokens: StravaTokenSet
      project_id: GCP Project ID
      bq_dataset: GCP BigQuery Dataset where tables will be stored
    """

    tokens: StravaTokenSet
    project_id: str
    bq_dataset: str


def load_config() -> AppConfig:
    """Load application configuration from environment and dotenv files.

    Loads configuration values from multiple sources in priority order:
    1. .env.tests (base development variables)
    2. Environment variables (override development variables)
    3. .env.local (override everything for local development)

    Returns:
        AppConfig: Complete application configuration including Strava tokens
                  and Google Cloud Platform settings.

    Raises:
        KeyError: If required environment variables are missing.
    """
    secrets_path = os.environ.get(
        "STRAVA_SECRETS_PATH", "/etc/secrets/strava_auth.json"
    )
    strava_auth: dict[str, str] = {}
    if secrets_path and os.path.exists(secrets_path):
        with open(secrets_path, "r", encoding="utf-8") as fin:
            strava_auth = json.load(fin)
    config = {
        **dotenv_values(".env.tests"),  # load shared development variables
        **os.environ,  # override loaded values with environment variables
        **strava_auth,
        **dotenv_values(".env.local"),
    }

    # Validate required environment variables
    client_id_str = _get_required_env_var(config, "STRAVA_CLIENT_ID")
    refresh_token = _get_required_env_var(config, "STRAVA_REFRESH_TOKEN")
    client_secret = _get_required_env_var(config, "STRAVA_CLIENT_SECRET")
    project_id = _get_required_env_var(config, "GCP_PROJECT_ID")
    bq_dataset = _get_required_env_var(config, "GCP_BIGQUERY_DATASET")

    loaded_tokens = StravaTokenSet(
        client_id=int(client_id_str),
        refresh_token=refresh_token,
        client_secret=client_secret,
    )
    app_config = AppConfig(
        tokens=loaded_tokens,
        project_id=project_id,
        bq_dataset=bq_dataset,
    )
    return app_config


app_config = load_config()
