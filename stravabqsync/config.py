"""Token loader"""
import os
from typing import NamedTuple

from dotenv import dotenv_values


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
    config = {
        **dotenv_values(".env.tests"),  # load shared development variables
        **os.environ,  # override loaded values with environment variables
        # **strava_auth,
        **dotenv_values(".env.local"),
    }

    loaded_tokens = StravaTokenSet(
        client_id=config["STRAVA_CLIENT_ID"],
        refresh_token=config["STRAVA_REFRESH_TOKEN"],
        client_secret=config["STRAVA_CLIENT_SECRET"],
    )
    app_config = AppConfig(
        tokens=loaded_tokens,
        project_id=config["GCP_PROJECT_ID"],
        bq_dataset=config["GCP_BIGQUERY_DATASET"],
    )
    return app_config


app_config = load_config()
