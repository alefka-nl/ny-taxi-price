"""Environment-driven configuration for the NYC taxi pipeline."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _get_env(name: str, default: str) -> str:
    """Read an environment variable with a sensible default."""
    return os.getenv(name, default)


@dataclass(frozen=True)
class AzureConfig:
    """Runtime settings for Azure storage and project-specific paths."""

    storage_account: str = _get_env("AZURE_STORAGE_ACCOUNT", "nytaxistorage")
    container: str = _get_env("AZURE_STORAGE_CONTAINER", "taxi-data")
    raw_prefix: str = _get_env("AZURE_TAXI_RAW_PREFIX", "raw/taxi")
    bronze_prefix: str = _get_env("AZURE_TAXI_BRONZE_PREFIX", "bronze/taxi")
    silver_prefix: str = _get_env("AZURE_TAXI_CURATED_PREFIX", "silver/taxi")
    gold_prefix: str = _get_env("AZURE_TAXI_GOLD_PREFIX", "gold/taxi")
    ml_prefix: str = _get_env("AZURE_TAXI_ML_PREFIX", "ml/taxi")
    model_prefix: str = _get_env("AZURE_TAXI_MODEL_PREFIX", "ml/models/taxi_fare_lr")
    blob_connection_string: str = _get_env("AZURE_BLOB_CONNECTION_STRING", "")
    local_base_path: str = _get_env("LOCAL_BASE_PATH", "./data")


AZURE_CONFIG = AzureConfig()
