from functools import lru_cache

from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.adapters.gcp._repositories import WriteActivityRepo
from stravabqsync.config import app_config
from stravabqsync.ports.out.write import WriteActivity


@lru_cache(maxsize=1)
def make_bigquery_client_wrapper() -> BigQueryClientWrapper:
    return BigQueryClientWrapper(project_id=app_config.project_id)


@lru_cache(maxsize=1)
def make_write_activity() -> WriteActivity:
    return WriteActivityRepo(make_bigquery_client_wrapper())
