from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataIngestionConfig,TraningPiplineConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
import sys

if __name__=='__main__':
    try:
        logging.info('************************************ Traning Pipline Started ************************************')
        traning_pipline_config=TraningPiplineConfig()

        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    
        data_ingestion_config=DataIngestionConfig(
            traning_pipline_config=traning_pipline_config
            )
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)
        data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()

        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Ingestion completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Validation Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        data_validation_config=DataValidationConfig(traning_pipline_config=traning_pipline_config)
        data_validation=DataValidation(
            training_pipeline_config=data_validation_config,
            data_ingestion_artifacts=data_ingestion_artifacts
            )
        data_validation_artifacts=data_validation.initiate_data_validation()
        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Validation completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Transformation Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        data_transformation_config=DataTransformationConfig(traning_pipline_config=traning_pipline_config)
        data_transformation=DataTransformation(
            data_transformation_config=data_transformation_config,
            data_validation_artifacts=data_validation_artifacts
            )
        data_transformation_artifacts=data_transformation.initate_data_transformation()

        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Data Transformation completed >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        logging.info(f'<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Model Train Started >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        model_trainer_config=ModelTrainerConfig(traning_pipline_config=traning_pipline_config)
        model_trainer=ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_tansformation_artifacts=data_transformation_artifacts
            )
        model_trainer.initate_model_traning()

        logging.info('************************************ Traning Pipline Completed ************************************')
    except Exception as e:
        logging.info(f' Error occured {str(e)}')
        raise CustomException(e,sys)    