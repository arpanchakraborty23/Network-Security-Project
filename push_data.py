from pymongo.mongo_client import MongoClient
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
import os,sys
import certifi
import json

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging


class NetworkDataExtract(): 
    def __init__(self) -> None:
        self.url=os.getenv('url')
        self.database=os.getenv('db')
        self.collection=os.getenv('collection')
        
        ca=certifi.where()
        logging.info('Loading Data to MongoDB')

    def csv_to_json(self,file_path):
        try:

            data= pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            data.head()

            json_data=list(json.loads(data.T.to_json()).values())
            return json_data

            l
        except Exception as e:
            logging.info('Error in data source')
            raise CustomException(sys,e)

    def insert_data_to_mongo_db(self,data):
        try:
            client=MongoClient(self.url)

            db=client[self.database]

            collection=db[self.collection]

            collection.insert_many(data)
            logging.info('store data to MongoDb DataBase successfully')
            
        except Exception as e:
            logging.info('Error in data pusher')
            raise CustomException(sys,e)

if __name__ == "__main__":
    filepath='Network_Data\phisingData.csv'
    load_obj=NetworkDataExtract()
    data=load_obj.csv_to_json(file_path=filepath)
    load_obj.insert_data_to_mongo_db(data=data)
