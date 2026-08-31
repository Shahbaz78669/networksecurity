import pandas as pd 
import numpy as np
import sys
import os



TRAGET_COLUMN = "Result"
PIPELINE_NAME:str  = "NetworkSecurity"
ARTIFACT_DIR :str = "Artifact"
FILE_NAME :str  = "PhisingData.csv"

TRAIN_FILE_NAME :str  = 'train.csv'
TEST_FILE_PATH :str = 'test.csv'


DATA_INGESTION_COLLECTION_NAME :str = 'Networkdata'
DATA_INGESTION_DATABASE_NAME:str  = 'NetworkSecurity'
DATA_INGESTION_DIR_NAME:str  = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str  = 'feature_store'
DATA_INGESTION_INGESTED_DIR :str  = 'ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO :float = 0.2