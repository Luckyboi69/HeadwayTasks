from flask import Flask, request, jsonify
import os
import pickle
import pandas as pd
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics.pairwise import manhattan_distances
from sklearn.neighbors import KNeighborsClassifier
app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data and model name from the request
        data = request.get_json()
        # Load the specified model
        model_name = 'calibrated_tpot_model'     
        with open(model_name, 'rb') as model_file:
            model = pickle.load(model_file) 
        # Ensure there's no nulls
        df=pd.DataFrame(data)
        df.fillna(df.mean(),inplace=True)
        # Perform prediction using the loaded model
        prediction = model.predict_proba(df)
        # Prepare the response to get only the positive class
        positive_class = [row[1] for row in prediction]
        response = {'prediction': positive_class}

        return jsonify(response)

    except Exception as e:
        # Handle errors
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
