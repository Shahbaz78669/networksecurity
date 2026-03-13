from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)  # ✅ Bug 1 fixed
        data_ingestion = DataIngestion(dataingestionconfig)                # ✅ Bug 2 fixed
        logging.info("Initiate data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()   # ✅ Bug 3 fixed
        print(dataingestionartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)