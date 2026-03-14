from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation


if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)  # ✅ Bug 1 fixed
        data_ingestion = DataIngestion(dataingestionconfig)                # ✅ Bug 2 fixed
        logging.info("Initiate data Ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()   # ✅ Bug 3 fixed
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation COmpleted")
        print(data_validation_artifact)



    except Exception as e:
        raise NetworkSecurityException(e, sys)