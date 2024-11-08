from datetime import datetime
from networksecurity.constant import traning_pipline
import os

class TraningPiplineConfig:
    def __init__(self) -> None:
      self.pipline_name=traning_pipline.PIPELINE_NAME   
      self.artifact_name=traning_pipline.ARTIFACT_DIR
      self.artifact_dir=os.path.join(self.artifact_name)
      
class DataIngestionConfig:
      def __init__(self,traning_pipline_config:TraningPiplineConfig) -> None:
         self.data_ingestion_dir:str=os.path.join(
            traning_pipline_config.artifact_dir, traning_pipline.DATA_INGESTION_DIR_NAME ## creating data ingestion dir inside artifacts
			)
         self.feature_store_file_path:str=os.path.join(
            traning_pipline_config.artifact_dir, traning_pipline.DATA_INGESTION_FEATURE_STORE_DIR ,traning_pipline.FILE_NAME ## saving raw data in artifact with file name
			)
         self.traning_data_store_path:str=os.path.join(
            traning_pipline_config.artifact_dir, traning_pipline.DATA_INGESTION__DIR, traning_pipline.TRAIN_FILE_NAME  ## artifacts folder , ingest folder , train data path
			)
         self.test_data_store_path:str=os.path.join(
            traning_pipline_config.artifact_dir,traning_pipline.DATA_INGESTION__DIR, traning_pipline.TEST_FILE_NAME ## artifacts folder , ingest folder , test data path
			)
         self.train_test_split_ratio:float=traning_pipline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
         