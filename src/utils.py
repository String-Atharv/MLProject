import os
import sys
from src.logger import logging
from src.exception import CustomException
from sklearn.metrics import r2_score
import os

import pandas as pd
import numpy as np
import dill

def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path) # getting the directory path from the file path
        os.makedirs(dir_path,exist_ok=True) # ensuring that the directory exists

        with open(file_path,'wb') as file_obj: # opening the file in write binary mode to save the object
            dill.dump(obj,file_obj) # saving the object to the file using dill

    except Exception as e:
        raise CustomException(e,sys)
    

def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report={}
        for i in range(len(models)):
            model=list(models.values())[i] # getting the model object from the models dictionary
            model.fit(X_train,y_train) # fitting the model to the training data
            y_test_pred=model.predict(X_test) # predicting the target values for the test data
            test_model_score=r2_score(y_test,y_test_pred) # calculating the r2 score for the test data
            report[list(models.keys())[i]]=test_model_score # adding the r2 score to the report dictionary with the model name as the key

        return report

    except Exception as e:
        raise CustomException(e,sys)