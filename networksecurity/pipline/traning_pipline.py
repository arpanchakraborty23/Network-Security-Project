import os
import sys
from datetime import datetime
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import DataIngestionConfig,TraningPiplineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.constant.traning_pipline import TRANING_S3_BUCKER
from networksecurity.cloud.s3_syncer import S3Sync
class TraningPipline:
    def __init__(self) -> None:
        self.traning_pipline_config=TraningPiplineConfig()
        self.s3_sync=S3Sync()

    def start_data_ingestion(self):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            start_data_ingestion_config=DataIngestionConfig(traning_pipline_config=self.traning_pipline_config)
            data_ingestion=DataIngestion(data_ingestion_config=start_data_ingestion_config)
            data_ingestion_artifats=data_ingestion.initiate_data_ingestion()

            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            return data_ingestion_artifats
        except Exception as e:
            logging.info(f'Error in data ingestion {str(e)}')
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifacts:DataIngestionArtifact):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Validation Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            data_validation_config=DataValidationConfig(traning_pipline_config=self.traning_pipline_config)
            data_validation=DataValidation(
                training_pipeline_config=data_validation_config,
                data_ingestion_artifacts=data_ingestion_artifacts
                )
            data_validation_artifacts=data_validation.initiate_data_validation()
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Validation completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            
            return data_validation_artifacts
        
        except Exception as e:
            logging.info(f'Error in data validation {str(e)}')
            raise CustomException(e,sys)
        
    def start_data_transformation(self,data_validation_artifacts:DataValidationArtifact,):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Transformation Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            data_transformation_config=DataTransformationConfig(traning_pipline_config=self.traning_pipline_config)
            data_transformation=DataTransformation(
                data_transformation_config=data_transformation_config,
                data_validation_artifacts=data_validation_artifacts
                )
            data_transformation_artifacts=data_transformation.initate_data_transformation()

            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Transformation completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

            return data_transformation_artifacts
        except Exception as e:
            logging.info(f'Error in data transformation {str(e)}')
            raise CustomException(e,sys)
        
    def start_model_train(self,data_transformation_artifacts:DataTransformationArtifact):
        try:
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Model Train Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            model_trainer_config=ModelTrainerConfig(traning_pipline_config=self.traning_pipline_config)
            model_trainer=ModelTrainer(
                model_trainer_config=model_trainer_config,
                data_tansformation_artifacts=data_transformation_artifacts
                )
            model_trainer_artifacts=model_trainer.initate_model_traning()
            logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Model Train Completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            return model_trainer_artifacts
            
        except Exception as e:
            logging.info(f'Error in model train {str(e)}')
            raise CustomException(e,sys)
    
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url=f's3://{TRANING_S3_BUCKER}/Artifacts/{self.traning_pipline_config.timestamp}'
            self.s3_sync.sync_folder_to_s3(folder=self.traning_pipline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
        
    def sync_final_model_dir_to_s3(self):
        try:
            aws_bucket_url=f's3://{TRANING_S3_BUCKER}/final_model/{self.traning_pipline_config.timestamp}'
            self.s3_sync.sync_folder_to_s3(folder=self.traning_pipline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
    
    def run_pipline(self):
        try:
            logging.info('************************************ Traning Pipline Started ************************************')
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifacts=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifacts=data_validation_artifact)
            model_trainer_artifact=self.start_model_train(data_transformation_artifacts=data_transformation_artifact)

            self.sync_artifact_dir_to_s3()
            self.sync_final_model_dir_to_s3()
            logging.info('************************************ Traning Pipline Completed ************************************')

            return model_trainer_artifact
        except Exception as e:
            logging.info(f'Error in traning pipline {str(e)}')
            raise CustomException(e,sys)
        