import os
import sys
import mlflow
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,BaggingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import mlflow.sklearn
from urllib.parse import urlparse
from flask import request
from mlflow.models import infer_signature
from dotenv import load_dotenv
load_dotenv

from networksecurity.utils.utills import save_obj,load_numpy_arr,model_evaluatuion,load_obj,save_as_json
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.ml_utils.metrics import get_classification_score 
from networksecurity.utils.ml_utils.model import NetworkModel


os.environ['MLFLOW_TRACKING_URI'] = os.getenv('MLFLOW_TRACKING_URI')
os.environ['MLFLOW_TRACKING_USERNAME'] = os.getenv('MLFLOW_TRACKING_USERNAME')
os.environ['MLFLOW_TRACKING_PASSWORD'] = os.getenv('MLFLOW_TRACKING_PASSWORD')

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_tansformation_artifacts:DataTransformationArtifact) -> None:
        
        self.model_trainer_config=model_trainer_config
        self.data_tansformation_artifacts=data_tansformation_artifacts

    def track_mlflow(self, best_model, clf_matric):
        try:
            logging.info('Starting MLflow tracking...')
            
            # Set the MLflow tracking URI from the environment variable
            mlflow_uri = os.getenv('MLFLOW_TRACKING_URI')
            if mlflow_uri is None:
                raise ValueError("MLFLOW_TRACKING_URI environment variable is not set.")
            mlflow.set_tracking_uri(mlflow_uri)

            # Start an MLflow run
            with mlflow.start_run(nested=True):
                # Extract and log classification metrics
                mlflow.log_metric('f1_score', clf_matric.f1_score)
                mlflow.log_metric('precision_score', clf_matric.precision_score)
                mlflow.log_metric('recall_score', clf_matric.recall_score)

                # Log the model with or without registration, based on URI type
                tracking_uri_type = urlparse(mlflow.get_tracking_uri()).scheme
                if tracking_uri_type != 'file':
                    mlflow.sklearn.log_model(best_model, 'model', registered_model_name='best_model')
                else:
                    mlflow.sklearn.log_model(best_model, 'model')

            logging.info('MLflow experiment tracking completed successfully.')

        except Exception as e:
            logging.info("An error occurred during MLflow tracking.",str(e))
            raise CustomException(e, sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            logging.info(' model evaluation started')
            models={
                'LogisticRegression':LogisticRegression(verbose=3),
                'KNeighborsClassifier': KNeighborsClassifier(),
                'DesisionTree':DecisionTreeClassifier(),
                'RandomForest':RandomForestClassifier(verbose=3),
                'BaggingClf':BaggingClassifier(verbose=3),
                'Xgboost':XGBClassifier()
            }
            params = {
                'LogisticRegression': {
                    'multi_class':['multinomial'],
                    'C': [1, 5, 10],
                    'penalty': ['l2'],
                
                },
                'KNeighborsClassifier': {
                    'n_neighbors': [1, 3, 5, 10],
                    'weights': ['uniform', 'distance'],
                    'metric': ['euclidean', 'manhattan']
                },
                'DesisionTree': {
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20],
                    # 'min_samples_split': [2, 5, 10],
                    # 'min_samples_leaf': [1, 2, 4]
                },
                'RandomForest': {
                    'n_estimators': [50, 100, 20],
                    # 'max_depth': [None, 10, 20],
                    # 'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                'BaggingClf': {
                    'n_estimators': [50, 100, 20],
                    'max_samples': [0.5, 0.7, 0.9]
                },
                'Xgboost': {
                    # 'n_estimators': [50, 100, 20],
                    # 'learning_rate': [0.01, 0.1,],
                    # 'max_depth': [3, 5, 7],
                    'subsample': [0.6, 0.8, 1.0],
                    'colsample_bytree': [0.6, 0.8, 1.0]
                }
            }
            model_report:dict=model_evaluatuion(x_train,y_train,x_test,y_test,models,params)
            print(model_report)
            logging.info(f'Model Report : {model_report}')

            print('\n====================================================================================\n')

            #  Find the best model
            best_model_score=max(sorted(model_report.values()))

            
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            # getting model traning metrices
            y_train_pred=best_model.predict(x_train)
            classification_traning_metrics=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            traning_scores={
                'f1_score':classification_traning_metrics.f1_score,'presision_score':classification_traning_metrics.precision_score,'recall_score':classification_traning_metrics.recall_score
                }
            save_as_json(obj=traning_scores,file_path=self.model_trainer_config.model_train_metrics_path)

            logging.info(f'Model traning report save successfully')

            ## Track training metrics with mlflow
            self.track_mlflow(best_model,classification_traning_metrics)
            mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI'))
            
            ## getting test metrices
            y_test_pred=best_model.predict(x_test)
            classification_test_metrics=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            test_scores={
                'f1_score':classification_test_metrics.f1_score,'presision_score':classification_test_metrics.precision_score,'recall_score':classification_test_metrics.recall_score
                }
            save_as_json(obj=test_scores,file_path=self.model_trainer_config.model_test_metrics_path)
            logging.info(f'Model test report save successfully')

            ## Track training metrics with mlflow
            self.track_mlflow(best_model,classification_test_metrics)
            
            print('metrices track successfully')
            
            
            preprocess_obj=load_obj(file_path=self.data_tansformation_artifacts.preprocess_obj_path)

           
            network_model=NetworkModel(
                processer=preprocess_obj,model=best_model
            )
             # saving best model
            save_obj(
                file_path=self.model_trainer_config.model_file_path,
                obj=network_model
            )
            logging.info(f'Model save in {self.model_trainer_config.model_file_path}')

            return classification_traning_metrics,classification_test_metrics
        
        except Exception as e:
            raise CustomException(e,sys)
        
      
    def initate_model_traning(self)->ModelTrainerArtifact:
        try:
            # data path
            train_array=self.data_tansformation_artifacts.train_arr_path
            test_array=self.data_tansformation_artifacts.test_arr_path

            # load data
            train_array=load_numpy_arr(train_array)
            test_array=load_numpy_arr(test_array)

            # split data 
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            classification_training_metrics,classification_test_metrics=self.train_model(x_train,y_train,x_test,y_test)
           
            model_trainer_artifacts=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.model_file_path,
                test_metric_artifact=classification_test_metrics,
                train_metric_artifact=classification_training_metrics
            )
            print('model traning completed')
            return model_trainer_artifacts

        except Exception as e:
            logging.info(f'Error in Model Traning {str(e)}')
            raise CustomException(e,sys)