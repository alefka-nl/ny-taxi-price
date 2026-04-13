# NYC Taxi Fare Prediction on Azure Synapse

## Overview

This repository contains an end-to-end data engineering and machine learning pipeline for predicting New York City yellow taxi fares at scale. The project is designed around Azure-native services and a medallion architecture implemented with PySpark and Delta Lake.

The workflow simulates ingestion through Azure Data Factory, persists raw data in Azure Data Lake Storage Gen2, transforms and enriches records in Azure Synapse Spark, and trains a regression model with Spark MLlib to predict taxi fares.

## Architecture

The target architecture follows this flow:

`Azure Data Factory -> Azure Data Lake Storage Gen2 -> Azure Synapse Analytics (PySpark + Delta Lake) -> ML model + predictions`

### High-level stages

1. Azure Data Factory orchestrates ingestion of external NYC taxi parquet files.
2. Raw parquet data lands in the `raw` zone of Azure Data Lake Storage.
3. Azure Synapse Spark notebooks process the raw layer into Bronze, Silver, and Gold Delta tables.
4. Spark MLlib trains a fare prediction model using engineered trip features.
5. Predictions and trained model artifacts are persisted back to storage for downstream consumption.

## Repository Structure

```text
project-root/
├── notebooks/
│   ├── 01_ingest.ipynb
│   ├── 02_transform.ipynb
│   ├── 03_ml.ipynb
├── src/
│   ├── config.py
│   ├── paths.py
│   ├── transform.py
│   ├── ml_pipeline.py
├── data/
├── requirements.txt
├── README.md
```

## Tech Stack

- Azure Data Factory
- Azure Data Lake Storage Gen2
- Azure Synapse Analytics
- PySpark
- Delta Lake
- Spark MLlib
- Python
- Azure Storage Blob SDK

## Medallion Architecture

### Bronze

The Bronze layer stores raw ingested taxi data with minimal modification. It preserves source fidelity and acts as the immutable landing zone for downstream processing.

### Silver

The Silver layer applies data quality rules and feature engineering. In this project it removes invalid fares, handles evolving schemas, and derives analytical features such as pickup hour.

### Gold

The Gold layer contains business-ready aggregates. Here it stores revenue summaries by pickup location for reporting and analytical use cases.

### ML

The ML layer contains prepared model inputs, prediction outputs, and serialized model artifacts. It enables both experimentation and downstream batch scoring scenarios.

## Machine Learning Pipeline

The model predicts `fare_amount` using the following features:

- `trip_distance`
- `PULocationID`
- `DOLocationID`
- `hour`

The training workflow:

1. Reads curated Silver data from Delta Lake.
2. Builds a Spark ML pipeline using feature assembly and linear regression.
3. Splits data into training and test sets.
4. Evaluates model quality with RMSE.
5. Writes prediction results to the `ml/` Delta path.
6. Saves the trained pipeline model to cloud storage.

## Configuration

The project uses environment variables for all runtime-sensitive configuration. No secrets are hardcoded.

Example variables:

```powershell
$env:AZURE_STORAGE_ACCOUNT="mystorageaccount"
$env:AZURE_STORAGE_CONTAINER="datalake"
$env:AZURE_TAXI_RAW_PREFIX="raw/taxi"
$env:AZURE_TAXI_CURATED_PREFIX="curated/taxi"
$env:AZURE_TAXI_GOLD_PREFIX="gold/taxi"
$env:AZURE_TAXI_ML_PREFIX="ml/taxi"
$env:AZURE_BLOB_CONNECTION_STRING="DefaultEndpointsProtocol=..."
```

## Running the Project

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Execute notebooks in order

1. `notebooks/01_ingest.ipynb`
2. `notebooks/02_transform.ipynb`
3. `notebooks/03_ml.ipynb`

### 3. Run in Synapse or local Spark

The code is structured so it can run in Azure Synapse Spark pools with ADLS paths, while still supporting local development through configurable base paths.

## Production Notes

- Secrets should be sourced from Azure Key Vault, Managed Identity, or Synapse linked services.
- Delta Lake is used for reliable incremental processing and schema evolution support.
- The source code under `src/` centralizes transformation and ML logic so notebook cells stay thin and reusable.
- The notebooks are written as orchestrated steps, mirroring a production data platform implementation.

## Future Improvements

- Add automated data quality checks with Great Expectations or Delta expectations.
- Introduce partitioning and Z-order optimization for larger-scale performance.
- Replace the baseline linear model with gradient-boosted trees or XGBoost on Spark.
- Add CI/CD for notebook deployment and Synapse artifacts.
- Register and version models in Azure Machine Learning or MLflow.
- Add batch and streaming ingestion patterns for near-real-time fare prediction.
