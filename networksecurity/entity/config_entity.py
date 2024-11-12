from datetime import datetime
from networksecurity.constant import traning_pipline
import os

class TraningPiplineConfig:
    def __init__(self) -> None:
      self.timestamp=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
      self.pipline_name=traning_pipline.PIPELINE_NAME   
      self.artifact_name=traning_pipline.ARTIFACT_DIR
      self.artifact_dir=os.path.join(self.artifact_name,self.timestamp)
      self.model_dir=os.path.join('final_model')
      
class DataIngestionConfig:
      def __init__(self,traning_pipline_config:TraningPiplineConfig) -> None:
         
         self.data_ingestion_dir:str=os.path.join(
            traning_pipline_config.artifact_dir, traning_pipline.DATA_INGESTION_DIR_NAME ## creating data ingestion dir inside artifacts
			)
         self.feature_store_file_path:str=os.path.join(
            self.data_ingestion_dir, traning_pipline.DATA_INGESTION_FEATURE_STORE_DIR ,traning_pipline.FILE_NAME ## saving raw data in artifact with file name
			)
         self.traning_data_store_path:str=os.path.join(
            self.data_ingestion_dir, traning_pipline.DATA_INGESTION__DIR, traning_pipline.TRAIN_FILE_NAME  ## artifacts folder , ingest folder , train data path
			)
         self.test_data_store_path:str=os.path.join(
            self.data_ingestion_dir,traning_pipline.DATA_INGESTION__DIR, traning_pipline.TEST_FILE_NAME ## artifacts folder , ingest folder , test data path
			)
         self.train_test_split_ratio:float=traning_pipline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
         
class DataValidationConfig:
    def __init__(self,traning_pipline_config:TraningPiplineConfig) -> None:
      self.data_validation_dir:str=os.path.join(
      	traning_pipline_config.artifact_dir,traning_pipline.DATA_VALIDATION_DIR_NAME ## crating data validaton folder inside artifacts
		)
      self.valid_dir_name:str=os.path.join(
         self.data_validation_dir, traning_pipline.DATA_VALIDATION_VALID_DIR ## validated report folder inside data validation folder
		)
      self.invalid_dir_name:str=os.path.join(
         self.data_validation_dir,traning_pipline.DATA_VALIDATION_INVALID_DIR ## invalid report folder inside data validation folder
		)
      self.drift_report_dir:str=os.path.join(
         self.data_validation_dir,traning_pipline.DATA_VALIDATION_DRIFT_REPORT_DIR,traning_pipline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME # data validation dir, drift report dir, report name
		)
      self.valid_traning_data_store_path:str=os.path.join(
         self.valid_dir_name, traning_pipline.TRAIN_FILE_NAME  ## artifacts folder , ingest folder , train data path
		)
      self.valid_test_data_store_path:str=os.path.join(
         self.valid_dir_name,traning_pipline.TEST_FILE_NAME ## artifacts folder , ingest folder , test data path
		)
      self.invalid_traning_data_store_path:str=os.path.join(
         self.valid_dir_name, traning_pipline.TRAIN_FILE_NAME  ## artifacts folder , ingest folder , train data path
		)
      self.invalid_test_data_store_path:str=os.path.join(
         self.valid_dir_name, traning_pipline.TEST_FILE_NAME ## artifacts folder , ingest folder , test data path
		)
      self.schema_file_path = os.path.join(
         traning_pipline.SCHEMA_File_DIR,traning_pipline.SCHEMA_File_NAME # schema file dir
      )

class DataTransformationConfig:
   def __init__(self,traning_pipline_config:TraningPiplineConfig) -> None:
      self.data_transformation_dir:str=os.path.join(
         traning_pipline_config.artifact_dir, traning_pipline.DATA_TRANSFORMATION_DIR_NAME ## creating data transformation dir name
      )
      self.data_transformation_train_path:str=os.path.join(
         self.data_transformation_dir,traning_pipline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,traning_pipline.DATA_TRANSFORMATION_TRANSFORMED_TRAIN_FILE_NAME # traning file path
      )
      self.data_transformation_test_path:str=os.path.join(
         self.data_transformation_dir,traning_pipline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,traning_pipline.DATA_TRANSFORMATION_TRANSFORMED_TEST_FILE_NAME ## test file path
      )
      self.preprocesss_file_path:str=os.path.join(
         self.data_transformation_dir,traning_pipline.PREPROCESSING_DIR_NAME,traning_pipline.PREPROCESSING_OBJECT_FILE_NAME ## preprocess file obj
      )

class ModelTrainerConfig:
   def __init__(self,traning_pipline_config:TraningPiplineConfig) -> None:
      self.model_triner_dir:str=os.path.join(
         traning_pipline_config.artifact_dir, traning_pipline.MODEL_TRINER_DIR_NAME ## creating model trainer dir
      )
      self.model_train_metrics_path:str=os.path.join(
         self.model_triner_dir,traning_pipline.MODEL_TRINER_MODEL_METRICS_DIR,traning_pipline.MODEL_TRINER_MODEL_TRAIN_METRICS_FILE
      )
      self.model_test_metrics_path:str=os.path.join(
         self.model_triner_dir,traning_pipline.MODEL_TRINER_MODEL_METRICS_DIR,traning_pipline.MODEL_TRINER_MODEL_TEST_METRICS_FILE
      )
      self.model_file_path=os.path.join(
         self.model_triner_dir,traning_pipline.MODEL_FILE_DIR,traning_pipline.MODEL_FILE_NAME
      )
      self.model_expacted_accuracy:float=traning_pipline.MODEL_TRINER_EXPACTED_ACCURCY
      self.model_overfitting_underfitting_ratio=traning_pipline.MODEL_TRINER_MODEL_OVERFITTING_UNDERFITTING_TH