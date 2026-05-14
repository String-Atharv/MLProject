import traceback
from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.logger import logger

application = Flask(__name__)
app = application

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            reading_score = int(request.form.get('reading_score'))
            writing_score = int(request.form.get('writing_score'))
            if not (0 <= reading_score <= 100 and 0 <= writing_score <= 100):
                return render_template('home.html', error="Scores must be between 0 and 100")
        except (ValueError, TypeError):
            return render_template('home.html', error="Please enter valid numeric scores")

        try:
            data=CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('race_ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=reading_score,
                writing_score=writing_score
            )
            pred_df=data.get_data_as_dataframe()
            logger.info(f"Prediction request received: {pred_df.to_dict()}")
            predict_pipeline=PredictPipeline()
            results=predict_pipeline.predict(pred_df)
            return render_template('home.html', result=results[0])
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            logger.error(traceback.format_exc())
            return render_template('home.html', error=f"Prediction failed: {e}")


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)
