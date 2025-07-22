from functools import lru_cache

from stravabqsync.adapters.gcp._clients import BigQueryClientWrapper
from stravabqsync.adapters.gcp._repositories import WriteActivitiesRepo
from stravabqsync.config import app_config
from stravabqsync.ports.out.write import WriteActivities


@lru_cache(maxsize=1)
def make_bigquery_client_wrapper() -> BigQueryClientWrapper:
    return BigQueryClientWrapper(project_id=app_config.project_id)


@lru_cache(maxsize=1)
def make_write_activities() -> WriteActivities:
    return WriteActivitiesRepo(
        client=make_bigquery_client_wrapper(), dataset_name=app_config.bq_dataset
    )
