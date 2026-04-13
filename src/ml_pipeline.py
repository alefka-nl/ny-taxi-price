"""Spark ML training utilities for taxi fare prediction."""

from __future__ import annotations

from typing import Tuple

from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql import DataFrame


FEATURE_COLUMNS = ["trip_distance", "PULocationID", "DOLocationID", "hour"]
LABEL_COLUMN = "fare_amount"


def train_fare_model(
    df: DataFrame,
    train_ratio: float = 0.8,
    seed: int = 42,
) -> Tuple[PipelineModel, DataFrame, float]:
    """
    Train a baseline Spark ML regression model and return predictions and RMSE.
    """
    assembler = VectorAssembler(
        inputCols=FEATURE_COLUMNS,
        outputCol="features",
        handleInvalid="skip",
    )
    regressor = LinearRegression(
        featuresCol="features",
        labelCol=LABEL_COLUMN,
        predictionCol="prediction",
    )

    pipeline = Pipeline(stages=[assembler, regressor])
    train_df, test_df = df.randomSplit([train_ratio, 1 - train_ratio], seed=seed)
    model = pipeline.fit(train_df)
    predictions = model.transform(test_df)

    evaluator = RegressionEvaluator(
        labelCol=LABEL_COLUMN,
        predictionCol="prediction",
        metricName="rmse",
    )
    rmse = evaluator.evaluate(predictions)
    return model, predictions, rmse
