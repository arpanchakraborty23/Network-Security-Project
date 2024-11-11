import os
import sys
import certifi
import pymongo
import pandas as pd
ca=certifi.where()
from dotenv import load_dotenv
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as run_app
from fastapi.responses import Response
from starlette.responses import RedirectResponse


from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.pipline.traning_pipline import TraningPipline
from networksecurity.utils.utills import load_obj,input_csv_to_db
from networksecurity.utils.ml_utils.model import NetworkModel

url = os.getenv('url')
database = os.getenv('db_pred')
collection = os.getenv('pred_collection')
print(url)

client=pymongo.MongoClient(url,tlsCAFile=ca)

app=FastAPI()
origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

from fastapi.templating import Jinja2Templates
templets=Jinja2Templates(directory='./templates')

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_route():
    try:
        traning_pipline=TraningPipline()
        traning_pipline.run_pipline()
        return Response('Traning comleted Successfully !')   
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post('/prediction')
async def prediction_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        print(df)
        preprocesser=load_obj('final_model\preprocesser.pkl')
        model=load_obj('final_model\model.pkl')
         # checking 'Unnamed: 0' col prasent or not
        if 'Unnamed: 0' in df.columns:
            print('Unnamed: 0 present in dataframe')
            df.drop(columns=['Unnamed: 0','Result'],axis=1,inplace=True)
        else:
            df.drop(columns='Result',axis=1,inplace=True)
            print(df.head(3))
        network_model=NetworkModel(preprocesser,model)
       

        y_pred=network_model.predict(df)
        print(y_pred)
        logging.info('prediction completed')

        df['predicted_col']=y_pred
        # data store in db
        input_csv_to_db(
            input_csv=df,url=url,db=database,collection=collection
        )

        table_html = df.to_html(classes='table table-striped')
        
        return templets.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise CustomException(e,sys)

if __name__ =="__main__":
    run_app(app=app,host='localhost',port=5000)