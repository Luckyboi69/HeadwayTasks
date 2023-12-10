from flask import Flask, request, jsonify
import os
import pandas as pd
import pickle
import mlflow
from mlflow.tracking import MlflowClient
from feature_extractor_module import FeatureExtractor

app = Flask(__name__)
feature_extractor = FeatureExtractor()

# Set the MLflow tracking URI

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
        data = request.get_json()

        model_name = data.get('dataset_id')
        start_timestamp = data.get('start_timestamp')
        test_dataset_path = data.get('test_dataset_path')

        start_timestamp = pd.to_datetime(start_timestamp)

        # Load the specified model using MLflow
        model, lags, intervals, features = load_model_from_mlflow(model_name)
        # Load the test dataset
        test_df = pd.read_csv(test_dataset_path)
        test_df['timestamp'] = pd.to_datetime(test_df['timestamp'])

        intervals = int(intervals)  # Convert 'intervals' to an integer if it's a string
        lags = int(lags)
        start_index = test_df[test_df['timestamp'] == start_timestamp].index[0]

        start_row = test_df.iloc[start_index :start_index + lags]
      
        features_= model.feature_names_in_
        df, _, _ = feature_extractor.extract_features(start_row, lags, intervals, features_)
        df.drop('value', axis=1, inplace=True)
             
        # Make predictions
        predictions = model.predict(df)

        # Prepare the response
        response = {
            'timestamps': df.index.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            'predictions':  predictions.tolist()#[predictions[-1]]  # Include only the prediction for the last row
        }


        return jsonify(response)

    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in prediction endpoint: {str(e)}")
        # Handle errors
        return jsonify({'error': str(e)}), 400


def load_model_from_mlflow(model_name):
    # Get the latest run for the specified model
    run_id, lags, intervals, features = get_latest_run_info(model_name)
    if run_id is None:
        raise ValueError(f'No runs found for model {model_name}')

    # Load the model from the MLflow server using the artifact path
    model_path = f"./mlruns/0/{run_id}/artifacts/{model_name}"
    model = mlflow.sklearn.load_model(model_path)

    return model, lags, intervals, features


def get_latest_run_info(model_name):
    # Get the latest run for the specified model
    client = MlflowClient()
    
    try:
        filter_string = f"tags.mlflow.runName='train_number_{model_name}'"
        runs = list(client.search_runs(
            experiment_ids=["0"],
            filter_string=filter_string,
            order_by=["start_time desc"],
            max_results=1
        ))

        if not runs:
            raise ValueError(f'No runs found for model {model_name}. Filter: {filter_string}')

        run_info = runs[0]
        run_id = run_info.info.run_id

        # Retrieve additional parameters from the run details
        run_details = client.get_run(run_id)
        lags = run_details.data.params.get("number_of_lags")
        intervals = run_details.data.params.get("interval")
        features = run_details.data.params.get("features")


        return run_id, lags, intervals, features
    except Exception as e:
        print(f"Error retrieving run information: {str(e)}")
        return None, None, None, None



def log_prediction_to_mlflow(model_name, prediction):
    # Log the prediction as a run in MLflow
    with mlflow.start_run():
        mlflow.set_tag("mlflow.runName","train_number_{model_name}")
        mlflow.log_param("prediction", prediction)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
