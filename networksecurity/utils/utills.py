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



@ensure_annotations
def read_yaml(file_path:Path):
    try:
        with open(file_path) as f:
            file=yaml.safe_load(f)
        return ConfigBox(file)
    except Exception as e:
        logging.info(f'error in {str(e)}')
        raise CustomException(sys,e)


@ensure_annotations   
def create_dir(file_path:list,verbose=True):
    try:
        for path in file_path:
            os.makedirs(path,exist_ok=True)
            if verbose:
                logging.info(f"created directory at: {path}")    
    except Exception as e:
        raise CustomException(sys,e) 
    
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
    with open(file_path,'wb') as f:
        pickle.dump(obj,f)

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


