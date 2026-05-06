import os
import sys
from src.logger import logging
from src.exception import CustomException

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
    

