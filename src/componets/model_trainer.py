from dataclasses import dataclass
import os
import sys
from src.logger import logger
from src.exception import CustomException
from src.utils import save_object
from sklearn.linear_model import Ridge,RidgeCV,Lasso,LassoCV,ElasticNet,ElasticNetCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor   
from sklearn.metrics import r2_score
from src.utils import evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path:str=os.path.join('artifacts','model.pkl') # path to save the trained model

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Ridge Regression":Ridge(),
                "Lasso Regression":Lasso(),
                "Elastic Net":ElasticNet(),
                "Decision Tree":DecisionTreeRegressor(),
                "Random Forest":RandomForestRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "AdaBoost":AdaBoostRegressor(),
                "Support Vector Regressor":SVR(),
                "K-Neighbors Regressor":KNeighborsRegressor(),
                "XGB Regressor":XGBRegressor(),
            }

            param = {

            "Ridge Regression": {
                'alpha': [0.1, 1.0, 10.0],
                'solver': ['auto', 'svd', 'cholesky', 'lsqr']
            },

            "Lasso Regression": {
                'alpha': [0.001, 0.01, 0.1, 1.0],
                'selection': ['cyclic', 'random']
            },

            "Elastic Net": {
                'alpha': [0.001, 0.01, 0.1, 1.0],
                'l1_ratio': [0.1, 0.5, 0.9]
            },

            "Decision Tree": {
                'max_depth': [None, 3, 5, 10],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
                'criterion': ['squared_error', 'friedman_mse', 'absolute_error'],
                'splitter': ['best', 'random']
            },

            "Random Forest": {
                'n_estimators': [50, 100],
                'max_depth': [None, 5, 10],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2],
                'max_features': ['sqrt', 'log2'],
                'bootstrap': [True]
            },

            "Gradient Boosting": {
                'n_estimators': [50, 100],
                'learning_rate': [0.05, 0.1],
                'max_depth': [3, 5],
                'min_samples_split': [2, 5],
                'min_samples_leaf': [1, 2]
            },

            "AdaBoost": {
                'n_estimators': [50, 100],
                'learning_rate': [0.05, 0.1, 1.0],
                'loss': ['linear', 'square']
            },

            "Support Vector Regressor": {
                'C': [0.1, 1, 10],
                'gamma': ['scale', 'auto'],
                'kernel': ['rbf', 'linear'],
                'epsilon': [0.1, 0.2]
            },

            "K-Neighbors Regressor": {
                'n_neighbors': [3, 5, 7],
                'weights': ['uniform', 'distance'],
                'p': [1, 2]
            },

            "XGB Regressor": {
                'n_estimators': [50, 100],
                'learning_rate': [0.05, 0.1],
                'max_depth': [3, 5],
                'min_child_weight': [1, 3],
                'subsample': [0.8, 1.0],
                'colsample_bytree': [0.8, 1.0]
            }
    }

            model_report:dict =evaluate_models(x_train,y_train,x_test,y_test,models,param)
            best_model_score = max(sorted(model_report.values()))

            # get the name of best model
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model=models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found with R2 score greater than 0.6",sys)
            logger.info("Best model found on both training and testing dataset {0} with R2 score: {1}".format(best_model_name,best_model_score))

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(x_test)
            r2_square=r2_score(y_test,predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)

