from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataTransformationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModeltrainerConfig,ModelTrainer


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
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info('Data transformation started')
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info('Data transformation completed')

        logging.info("Model Trianer started")
        model_trainer_config=ModeltrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")






    except Exception as e:
        raise NetworkSecurityException(e, sys)