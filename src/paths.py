"""Path helpers that support Azure and local execution modes."""

from __future__ import annotations

import os

from src.config import AZURE_CONFIG


USE_LOCAL = os.getenv("USE_LOCAL_PATHS", "false").lower() == "true"


def _azure_path(prefix: str) -> str:
    return (
        f"abfss://{AZURE_CONFIG.container}@{AZURE_CONFIG.storage_account}"
        f".dfs.core.windows.net/{prefix.strip('/')}/"
    )


def _local_path(prefix: str) -> str:
    return os.path.join(AZURE_CONFIG.local_base_path, prefix.strip("/")).replace("\\", "/") + "/"


BASE_PATH = AZURE_CONFIG.local_base_path if USE_LOCAL else _azure_path(AZURE_CONFIG.raw_prefix)
RAW_PATH = _local_path(AZURE_CONFIG.raw_prefix) if USE_LOCAL else _azure_path(AZURE_CONFIG.raw_prefix)
BRONZE_PATH = _local_path(AZURE_CONFIG.bronze_prefix) if USE_LOCAL else _azure_path(AZURE_CONFIG.bronze_prefix)
SILVER_PATH = _local_path(AZURE_CONFIG.silver_prefix) if USE_LOCAL else _azure_path(AZURE_CONFIG.silver_prefix)
GOLD_PATH = _local_path(AZURE_CONFIG.gold_prefix) if USE_LOCAL else _azure_path(AZURE_CONFIG.gold_prefix)
ML_PATH = _local_path(AZURE_CONFIG.ml_prefix) if USE_LOCAL else _azure_path(AZURE_CONFIG.ml_prefix)
MODEL_PATH = _local_path(AZURE_CONFIG.model_prefix) if USE_LOCAL else _azure_path(AZURE_CONFIG.model_prefix)
