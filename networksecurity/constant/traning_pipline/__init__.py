import os
import sys 
import pandas as pd 
import numpy as np

""" 
define common constant variable for traing pipline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_File_DIR: str='schema_data'
SCHEMA_File_NAME: str='schema.yaml'

PREPROCESSING_DIR_NAME: str = "preprocesser"
PREPROCESSING_OBJECT_FILE_NAME: str = "preprocessing.pkl"

""" 
    Data Ingestion related constant 
"""

DATA_INGESTION_DIR_NAME:str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION__DIR:str='ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.26

""" 
   Data VALIDATION related constant 
"""
DATA_VALIDATION_DIR_NAME:str='data_validation'
DATA_VALIDATION_VALID_DIR:str='validated'
DATA_VALIDATION_INVALID_DIR:str='invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR:str='drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str='report.yaml'

""" 
   Data Transformation related constant 
"""
DATA_TRANSFORMATION_DIR_NAME:str='data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str='transformed'
DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME:str='test.npy'
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME:str='train.npy'

DATA_TRANSFORMATION_IMPUTE_PARAMS:dict={
    'missing_values':np.nan,
    'n_neighbors':3,
    'weights':'uniform'
}