import os,sys
import pandas as pd, numpy as np
from networksecurity.components.data_validation import DataValidation,DataValidationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.impute import KNNImputer
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_obejct
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORAMTION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig,DataValidationConfig


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        



    def get_data_transformer_obj(self)->Pipeline:
        logging.info("Entered the data_transformation object function")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORAMTION_IMPUTER_PARAMS)
            logging.info(f"Initialised KNNImputer with {DATA_TRANSFORAMTION_IMPUTER_PARAMS}")
            Processor:Pipeline=Pipeline([("imputer",imputer)])
            return Processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
       



    def initiate_data_tramsformation(self)->DataTransformationArtifact:
        logging.info("ENtered intiate data transformation ")
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            if TARGET_COLUMN not in train_df.columns and "class" in train_df.columns:
                train_df.rename(columns={"class": TARGET_COLUMN}, inplace=True)
            if TARGET_COLUMN not in test_df.columns and "class" in test_df.columns:
                test_df.rename(columns={"class": TARGET_COLUMN}, inplace=True)

            #training dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            #test data frame
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            preprocessor_object=self.get_data_transformer_obj()
            preprocessor_object.fit(input_feature_train_df)
            transformed_input_train_df=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_df=preprocessor_object.transform(input_feature_test_df)

            train_array=np.c_[
                transformed_input_train_df,np.array(target_feature_train_df)
            ]
            test_array=np.c_[
                transformed_input_test_df,np.array(target_feature_test_df)
            ]

            save_numpy_array_data(self.data_transformation_config.trasformed_train_file_path,array=train_array)

            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_array)
            save_obejct(self.data_transformation_config.transformed_object_file_path,preprocessor_object)


            logging.info("Preparing artifact")
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_trained_file_path=self.data_transformation_config.trasformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            return data_transformation_artifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)
        












