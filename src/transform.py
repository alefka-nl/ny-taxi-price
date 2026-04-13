"""Reusable PySpark transformations for the NYC taxi pipeline."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def clean_taxi_data(df: DataFrame) -> DataFrame:
    """Remove obviously invalid records and standardize null handling."""
    return (
        df.filter(F.col("fare_amount").isNotNull())
        .filter(F.col("fare_amount") >= 0)
        .filter(F.col("trip_distance").isNotNull())
        .filter(F.col("tpep_pickup_datetime").isNotNull())
    )


def add_time_features(df: DataFrame) -> DataFrame:
    """Add the hour of pickup for downstream analytics and modeling."""
    return df.withColumn("hour", F.hour(F.col("tpep_pickup_datetime")))


def select_model_columns(df: DataFrame) -> DataFrame:
    """Select the minimal set of columns needed for model training."""
    return df.select(
        "fare_amount",
        "trip_distance",
        "PULocationID",
        "DOLocationID",
        "hour",
    ).dropna()


def aggregate_revenue_by_location(df: DataFrame) -> DataFrame:
    """Build a Gold-layer aggregate for revenue analysis by pickup location."""
    return (
        df.groupBy("PULocationID")
        .agg(
            F.sum("fare_amount").alias("total_revenue"),
            F.count("*").alias("trip_count"),
            F.avg("fare_amount").alias("avg_fare_amount"),
        )
        .orderBy(F.desc("total_revenue"))
    )
