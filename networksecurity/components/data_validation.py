from  networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestionConfig
from networksecurity.components.data_ingestion import DataIngestionConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import wirte_yaml_file
import os
import sys
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
from networksecurity.utils.main_utils.utils import read_yaml_file





class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
          return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)




    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_pf_columns=len(self.schema_config)
            if(number_pf_columns==len(dataframe.columns)):
                return True
            else :
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            # Get expected numerical columns from schema
            numerical_columns = [col for col in self.schema_config.keys() 
                            if self.schema_config[col] == 'numerical']  # Adjust based on your schema format
            
            # Check if all expected numerical columns exist
            existing_columns = set(dataframe.columns)
            missing_numerical = [col for col in numerical_columns if col not in existing_columns]
            
            if missing_numerical:
                logging.warning(f"Missing numerical columns: {missing_numerical}")
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)



    def is_data_drift_present(self,prev_df,curr_df,threshold=0.05)->bool:
        try:
            report={}
            for column in prev_df.columns:
                d1=prev_df[column]
                d2=curr_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else :
                    is_found=True
                    status=False
                report.update({column:{"p_value":float(is_same_dist.pvalue),"drift_status":is_found}})

                drift_report_file_path=self.data_validation_config.drift_report_file_path

                #creating directory
                dir_path=os.path.dirname(drift_report_file_path)
                os.makedirs(dir_path,exist_ok=True)
                wirte_yaml_file(drift_report_file_path,report)

                
                




        except Exception as e:
            raise NetworkSecurityException(e,sys)

        


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message=""

            
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_data_frame=DataValidation.read_data(train_file_path)
            test_data_frame=DataValidation.read_data(test_file_path)

            #validatinf number of columns
            train_status=self.validate_number_of_columns(train_data_frame)
            test_status=self.validate_number_of_columns(test_data_frame)
            if not train_status:
                error_message=f"{error_message} train data frame does not conain all the columns"
            if not test_status:
                error_message=f"{error_message} test data frame does not conatin all the columns"
                status=self.is_data_drift_present(train_data_frame,test_data_frame)
                dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path,exist_ok=True)
                train_data_frame.to_csv(
                    self.data_validation_config.valid_train_file_path,index=False,header=True
                )
                test_data_frame.to_csv(
                    self.data_validation_config.valid_test_file_path,index=False,header=True
                )


                data_validation_artifact=DataValidationArtifact(
                    data_validation_status=status,
                    valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                    valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=None,
                    invalid_test_file_path=None,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path


                )
                return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

        