import os 
import sys
import pandas as pd
import numpy as np
import pymongo
from networksecurity.logging.logger import logging
from sklearn.model_selection import train_test_split
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from dotenv import load_dotenv
load_dotenv()
from networksecurity.entity.artifact_entity import DataIngestionArtifact













MONGO_DB_URL=os.getenv("MONGO_DB_URL")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:  

    
           self.data_ingestion_config=data_ingestion_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def export_data_from_mongodb_as_dataframe(self):



        ''' Read the data from mongodb'''
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
                df.replace({"na":np.nan},inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:

    
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def initiate_train_test_split(self,dataframe:pd.DataFrame):
        try:
            logging.info("Splitting the data into train set and test set")
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            training_file_path=self.data_ingestion_config.training_dir
            testing_file_path=self.data_ingestion_config.testing_dir
            train_dir_path=os.path.dirname(training_file_path)
            test_dir_path=os.path.dirname(testing_file_path)


            logging.info("making the directories of test and train file path")
            os.makedirs(train_dir_path,exist_ok=True)
            os.makedirs(test_dir_path,exist_ok=True)
            logging.info("Directories of test and train file path created ")

            train_set.to_csv(
                self.data_ingestion_config.training_dir,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_dir,index=False,header=True
            )

            logging.info("Expoted train and test file paths")


        except Exception as e:
            raise NetworkSecurityException(e,sys)




    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_data_from_mongodb_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.initiate_train_test_split(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_dir,test_file_path=self.data_ingestion_config.testing_dir)
            return data_ingestion_artifact





        except Exception as e:
            raise NetworkSecurityException(e,sys)

