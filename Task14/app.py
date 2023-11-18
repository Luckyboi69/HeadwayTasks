from flask import Flask, request, jsonify
import os
import pandas as pd
import pickle
from feature_extractor_module import FeatureExtractor
app = Flask(__name__)
feature_extractor=FeatureExtractor()
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data and model name from the request
        data = request.get_json()
        model_name = data.get('dataset_id')
        # Load the specified model
        model_path = f'models/model_{model_name}.pkl'
        if not os.path.exists(model_path):
            return jsonify({'error': f'Model {model_name} not found'})

        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)            
        test_data=data.get('values')
        lags_value = get_lags_for_train_number(model_name)
        intervals= get_time_intervals_for_train_number(model_name)
        features= model.feature_names_in_
        df,o,p= feature_extractor.extract_features(test_data,lags_value,intervals,features)
        df.drop('value',axis=1,inplace=True)
        last_value=df.tail(1)
        print(last_value)
        #print(last_value)
        print("OOO",model_name)
        print(test_data)
        next_value_pred = model.predict(last_value)
        # Perform prediction using the loaded model
        # Prepare the response
        response = {'prediction': next_value_pred[0]}

        return jsonify(response)

    except Exception as e:
        # Handle errors
        return jsonify({'error': str(e)})
def get_lags_for_train_number(train_number):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('./train_lags.csv')

    # Find the row corresponding to the given train_number
    row = df[df['train_number'] == train_number]

    # If the train_number is found, return the corresponding lags value
    if not row.empty:
        return row['lags'].values[0]
    else:
        # Handle the case where the train_number is not found
        print(f"Train number {train_number} not found in the CSV.")
        return None
def get_time_intervals_for_train_number(train_number):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('./timestamp_intervals.csv')

    # Find the row corresponding to the given train_number
    row = df[df['train_number'] == train_number]

    # If the train_number is found, return the corresponding lags value
    if not row.empty:
        return row['timestamp_intervals'].values[0]
    else:
        # Handle the case where the train_number is not found
        print(f"Train number {train_number} not found in the CSV.")
        return None    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
