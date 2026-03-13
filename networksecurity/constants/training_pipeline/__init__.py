import pandas as pd
import numpy as np
import sys
import os

''' defining common constants'''
TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
AIRTIFACT_DIR:str="Airtifacts"
FILE_NAME:str="uci-ml-phishing-dataset.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"


''' DATA Ingestion related constant start with DATA_INGESTION VAR NAME'''
DATA_INGESTION_COLLECTION_NAME: str="NetworkData"
DATA_INGESTION_DATABASE_NAME: str="SHAHBAZAI"
DATA_INGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2