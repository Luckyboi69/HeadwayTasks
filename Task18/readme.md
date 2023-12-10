## To run the app use docker-compose up , then send json requests through Postman http://127.0.0.1:5000/predict

# 1- feature_extractor_module.py
This file contains FeatureExtractor Class which is responsible for the preprocessing & feature extraction needed for both train and test data
we extract some features from the timestamp , then calculate the moving average after that the lagged features and lastly some features from prophet 
keep in mind that all features added must have a correlation with the target value greater or equal to 20% except the lagged features we always add at least 1 and the same goes for moving average it's always calculated

# 2- train_models.py
This file trains linear regression models and saves them in seperate runs using MlFlow saving the params of the lags required and the intervals in minutes which are called when predicting

# 3- app.py
Here Flask is used to create a post request with the function predict that takes the post data and then reads the corresponding model relevant to the dataset id which is the same as model name in mlflow run after that it loads it's timestamp interval and the lag number('which is equivalent to the needed values to input'), and it loads the features of the old model then passes it all to the feature extraction class then the returned dataframe the 'value' column is dropped and the last row is passed to the model.predict() and the prediction is returned 

