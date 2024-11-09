import os
import sys

from networksecurity.constant.traning_pipline import MODEL_FILE_DIR,MODEL_FILE_NAME
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

class NetworkModel:
    def __init__(self,processer,model) -> None:
        self.processer=processer
        self.model=model


    def predict(self,x):
        try:
            x_transform=self.processer.transform(x)
            y_pred=self.model.predict(x_transform)

            return y_pred
        except Exception as e:
            raise CustomException(e,sys)