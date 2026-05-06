import os
import sys
from dataclasses import dataclass

from sklearn.impute import SimpleImputer
from src.exception import CustomException
from src.logger import logger
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
import numpy as np
import pandas as pd
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path:str=os.path.join('artifacts','preprocessor.pkl') # path to save the preprocessing file to preprocess the data

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        ''' This function is responsible for data transformation and returns the preprocessor object to preprocess the data'''
        try:
            numerical_features=['reading score','writing score']
            categorical_features=['gender','race/ethnicity','parental level of education','lunch','test preparation course']
            
            numerical_pipeline=Pipeline([('imputer',SimpleImputer(strategy='median')),('scaler',StandardScaler())]) # pipeline for numerical features to scale the data

            categorical_pipeline=Pipeline([('imputer',SimpleImputer(strategy='most_frequent')),('one_hot_encoder',OneHotEncoder()),('scaler',StandardScaler(with_mean=False))]) # pipeline for categorical features to one hot encode the data and then scale it

            preprocessor=ColumnTransformer([('numerical_pipeline',numerical_pipeline,numerical_features),('categorical_pipeline',categorical_pipeline,categorical_features)]) # combining the numerical and categorical pipelines

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Read train and test data completed")

            logger.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name ="math score"

            # Splitting input and target features for train
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            # Splitting input and target features for test
            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            logger.info(
                "Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr,
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                input_feature_test_arr,
                np.array(target_feature_test_df)
            ]

            logger.info("Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)