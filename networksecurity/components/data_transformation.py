import os
import sys
import numpy as np
import pandas as pd
import pickle
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,RobustScaler

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.utils.utills import save_obj,save_numpy_arr
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.constant.traning_pipline import TARGET_COLUMN
from networksecurity.constant.traning_pipline import DATA_TRANSFORMATION_IMPUTE_PARAMS


class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig) -> None:
        self.data_validation_artifacts=data_validation_artifacts
        self.data_transformaation_config=data_transformation_config

    @staticmethod
    def read_data(data: str)-> pd.DataFrame:
        return pd.read_csv(data)

    @staticmethod
    def preprocess_obj()-> Pipeline:
        try:
            preprocess_obj:Pipeline=Pipeline(
                steps=[
                    ('impute',KNNImputer(**DATA_TRANSFORMATION_IMPUTE_PARAMS)),
                    ('scaling',RobustScaler())
                ]
            )
            logging.info('preprocess object created')

            return preprocess_obj
        except Exception as e:
            raise CustomException(e,sys)
        
    def initate_data_transformation(self)->DataTransformationArtifact:
        try:
            train_data_path=self.data_validation_artifacts.valid_train_path
            test_data_path=self.data_validation_artifacts.valid_test_path

            train_df=self.read_data(data=train_data_path)
            test_df=self.read_data(data=test_data_path)
            logging.info('data read completed')
            print(train_df.head())

            ## traning dataframe
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1) # x_train

            Target_feature_train_df=train_df[TARGET_COLUMN] # y_train
            Target_feature_train_df=Target_feature_train_df.replace(-1,0)

            ## test dataframe
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1) # x_test
            Target_feature_test_df=test_df[TARGET_COLUMN]
            Target_feature_test_df=Target_feature_test_df.replace(-1,0)

            ## data preprocessing
            preprocess_obj=self.preprocess_obj()

            transform_input_feature_train_df=preprocess_obj.fit_transform(input_feature_train_df)
            transform_input_feature_test_df=preprocess_obj.transform(input_feature_test_df)

            logging.info('data preprocessing completed')

            train_arr=np.c_[transform_input_feature_train_df,np.array(Target_feature_train_df)]
            save_numpy_arr(file=self.data_transformaation_config.data_transformation_train_path,arr=train_arr)

            test_arr=np.c_[transform_input_feature_test_df,np.array(Target_feature_test_df)]
            save_numpy_arr(file=self.data_transformaation_config.data_transformation_test_path,arr=test_arr)

            save_obj(
                file_path=self.data_transformaation_config.preprocesss_file_path,
                obj=preprocess_obj
            )
            
            ## final model
            save_obj(file_path='final_model/preprocesser.pkl',obj=preprocess_obj)
            print('preprocesser save successfully')
            data_transformation_artifacts=DataTransformationArtifact(
                train_arr_path=self.data_transformaation_config.data_transformation_train_path,
                test_arr_path=self.data_transformaation_config.data_transformation_test_path,
                preprocess_obj_path=self.data_transformaation_config.preprocesss_file_path
            )
            print('Data transformation artifacts created')
            logging.info('Data transformation artifacts created')
            
            return data_transformation_artifacts

        except Exception as e:
            logging.info(f'Error in Data transformation {str(e)}')
            raise CustomException(sys,e)