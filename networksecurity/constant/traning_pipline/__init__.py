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