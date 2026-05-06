import sys
import os
import pandas as pd
from src.logger import logger
from src.exception import CustomException
from src.utils import load_object

# Resolve artifact paths relative to project root, not cwd
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREPROCESSOR_PATH = os.path.join(BASE_DIR, 'artifacts', 'preprocessor.pkl')
MODEL_PATH = os.path.join(BASE_DIR, 'artifacts', 'model.pkl')

class PredictPipeline:
    _preprocessor = None
    _model = None

    @classmethod
    def _load_artifacts(cls):
        """Load model and preprocessor once, then cache for subsequent requests."""
        if cls._preprocessor is None or cls._model is None:
            cls._preprocessor = load_object(PREPROCESSOR_PATH)
            cls._model = load_object(MODEL_PATH)

    def predict(self, features):
        try:
            self._load_artifacts()

            data_scaled = self._preprocessor.transform(features) # preprocessing the input features using the preprocessor object

            pred = self._model.predict(data_scaled) # making predictions using the trained model

            return pred
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int
    ):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race/ethnicity":[self.race_ethnicity],
                "parental level of education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test preparation course": [self.test_preparation_course],
                "reading score": [self.reading_score],
                "writing score": [self.writing_score]
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            raise CustomException(e, sys)
