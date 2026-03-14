import pandas as pd
import numpy as np
import sys
import os

''' defining common constants'''
TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="uci-ml-phishing-dataset.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

# SCHEMA_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..","..", "data_schema", "schema.yml")
SCHEMA_FILE_PATH = r"D:\NetworkSecurity\data_schema\schema.yaml"


''' DATA Ingestion related constant start with DATA_INGESTION VAR NAME'''
DATA_INGESTION_COLLECTION_NAME: str="NetworkData"
DATA_INGESTION_DATABASE_NAME: str="SHAHBAZAI"
DATA_INGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

''' Data Validation related constant start with DATA_VALIDATION VAR NAME'''

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yml"