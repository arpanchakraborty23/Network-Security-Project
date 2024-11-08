from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataIngestionConfig,TraningPiplineConfig
from networksecurity.components.data_ingestion import DataIngestion

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
import sys

if __name__=='__main__':
    try:
        logging.info(f'<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>')
        
        traning_pipline_config=TraningPiplineConfig()
        data_ingestion_config=DataIngestionConfig(traning_pipline_config=traning_pipline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion.initiate_data_ingestion()

        logging.info(f'<<<<<<<<<<<<<<<<<<<< Data Ingestion completed >>>>>>>>>>>>>>>>>>')
    except Exception as e:
        logging.info(f' Error occured {str(e)}')
        raise CustomException(e,sys)    