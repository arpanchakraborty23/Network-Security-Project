import os
import sys
import yaml,json
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from pathlib import Path
from ensure import ensure_annotations
from box import ConfigBox
from sklearn.metrics import roc_auc_score,accuracy_score
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from pymongo import MongoClient


def read_yaml(file_path:str):
    try:
        with open(file_path) as f:
            file=yaml.safe_load(f)
        return ConfigBox(file)
    except Exception as e:
        logging.info(f'error in {str(e)}')
        raise CustomException(sys,e)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)
    
def Data_read_from_db(url,db,collection):
    client=MongoClient(url)

    db=client[db]
    collection=db[collection]
    
    data=collection.find()
    df=pd.DataFrame(data)

    if'_id' in df.columns:
        df.drop('_id',axis=1,inplace=True)
    df.replace({'na':np.nan},inplace=True)
    print(df.head())
    return df

def input_csv_to_db(input_csv,url,db,collection):
    try:
        logging.info(type(input_csv))

        Client=MongoClient(url)
        db=Client[db]
        collection=db[collection]
        print(input_csv)
        dict_m=input_csv.to_dict(orient='records')
        collection.insert_many(dict_m)
        
    except Exception as e:
        logging.info(f'Error in {str(e)}')
        raise CustomException(sys,e) 
    
    
def save_obj(file_path,obj):
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    with open(file_path,'wb') as f:
        pickle.dump(obj,f)
    
        logging.info(f'{obj} save successfully')

def save_numpy_arr(file, arr):
    try:
        dir_path = os.path.dirname(os.path.abspath(file))
        os.makedirs(dir_path, exist_ok=True)
        # Save the numpy array
        with open(file, 'wb') as file:
            np.save(file, arr)
            print(f'Successfully saved array in {file}')
            logging.info(f'Successfully saved array in {file}')
            
    except Exception as e:
        raise CustomException(e, sys)
    
def load_numpy_arr(filepath):
    try:
        with open(filepath,'rb') as f:
            obj=np.load(f,allow_pickle=True)
            logging.info(f'{obj} load successfully ')
        return obj
    except Exception as e:
        raise CustomException(e,sys)

def model_evaluatuion(x_train,y_train,x_test,y_test,models,prams):
    try:
            logging.info(' model evaluation started')
            report={}
            for i in range(len(models)):
                model = list(models.values())[i]
                param=prams[list(models.keys())[i]]
                #prams=prams[list(models.keys())[i]]
                print(f"Training {model}...")
                gs=GridSearchCV(model,param_grid=param,cv=5,verbose=3,refit=True,scoring='neg_mean_squared_error',n_jobs=-1)

            
                gs.fit(x_train,y_train)

                model.set_params(**gs.best_params_)

                # Train model
                model.fit(x_train,y_train)

                

                # Predict Testing data
                y_test_pred =model.predict(x_test)

                
                test_model_score = accuracy_score(y_test,y_test_pred)*100

                print(f"Training {model} accuracy {test_model_score}")

                report[list(models.keys())[i]] =  test_model_score

            return report
        
    except Exception as e:
        logging.info(f' Error {str(e)}')
        raise CustomException(sys,e)
    
def load_obj(file_path):
    with open(file_path,'rb') as f:
        data=pickle.load(f)

    return data

def save_json(data,filename):
  
        with open(filename,'w') as j:
            json.dump(data,j,indent=4)


