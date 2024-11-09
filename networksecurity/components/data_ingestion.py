from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.utils.utills import Data_read_from_db
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()



class DataIngestion:
   def __init__(self,data_ingestion_config:DataIngestionConfig) -> None:
      self.config = data_ingestion_config
      self.url = os.getenv('url')
      self.database = os.getenv('db')
      self.collection = os.getenv('collection')

   def export_data_to_feature_store(self,df:pd.DataFrame) -> pd.DataFrame:
      try:
         logging.info('Storing raw data to feature store path')

         feature_store_dir_path:str=self.config.feature_store_file_path

         dir_path=os.path.dirname(feature_store_dir_path)
         os.makedirs(dir_path,exist_ok=True)

         df.to_csv(feature_store_dir_path,index=False,header=True)
         logging.info('Storing Raw data completed')
         return df
      
      except Exception as e:
         logging.info(f'Error in export data {str(e)}')
         raise CustomException(e,sys)
      
   def split_data_into_train_test(self,df):
      try:
         logging.info('spliting data to train set and test set')

         test_data,train_data=train_test_split(
            df,test_size=self.config.train_test_split_ratio,random_state=42
			)
         logging.info('Data split into training and testing sets successfully.')

         # saving train and test data
         train_dir_path=os.path.dirname(self.config.traning_data_store_path)
         os.makedirs(train_dir_path,exist_ok=True)
         train_data.to_csv(self.config.traning_data_store_path)

         test_dir_path=os.path.dirname(self.config.test_data_store_path)
         os.makedirs(test_dir_path,exist_ok=True)
         test_data.to_csv(self.config.test_data_store_path)

         logging.info(f'Training and test data saved to {self.config.traning_data_store_path} and {self.config.test_data_store_path} respectively.')
      except Exception as e:
         raise CustomException(e,sys)
   def initiate_data_ingestion(self):
      try:
         
         df=Data_read_from_db(url=self.url,db=self.database,collection=self.collection)

         self.export_data_to_feature_store(df=df)

         self.split_data_into_train_test(df=df)

         data_ingestion_artifacts=DataIngestionArtifact(
            trained_file_path=self.config.traning_data_store_path,
            test_file_path=self.config.test_data_store_path
			)
         return data_ingestion_artifacts
      
      except Exception as e:
         logging.info(f'Error in Data Ingestion: {str(e)}')
         raise CustomException(e,sys)
      