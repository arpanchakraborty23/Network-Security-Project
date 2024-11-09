from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_path:str
    valid_test_path:str
    invalid_train_path:str
    invalid_test_path:str
    drift_report_path:str

@dataclass
class DataTransformationArtifact:
    train_arr_path:str
    test_arr_path:str
    preprocess_obj_path:str
  

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path:str
    train_metric_artifact:dict
    test_metric_artifact:dict