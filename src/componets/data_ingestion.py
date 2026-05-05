import os
import sys
from src.logger import logger
from src.exception import CustomException
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join('artifacts','train.csv')
    test_data_path:str=os.path.join('artifacts','test.csv') 
    raw_data_path:str=os.path.join('artifacts','data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        logger.info("Data Ingestion method starts")
        try:
            df = pd.read_csv('notebook/data/StudentsPerformance.csv')## reading data from source
            logger.info("Dataset read as pandas dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #ensuring that directory exists

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True) # saving the raw data from source to the csv file in artifacts folder

            logger.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42) # splitting the data into train and test set

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True) # saving the train set to the csv file in artifacts folder
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True) # saving the test set to the csv file in artifacts folder

            logger.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path, # returning the path of the train and test data csv files
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        


if __name__ == "__main__":
            obj=DataIngestion()
            obj.initiate_data_ingestion()