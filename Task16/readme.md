## To run the app use docker-compose up , then send json requests through Postman http://127.0.0.1:5000/predict

# 1-AutoML_Session_Task.ipynb
 The model was trained using TPOT generating tpot_model and then Calibrated and saved finally as calibrated_tpot_model 

# 2- app.py
    Contains Flask and the predict endpoint, it handles nulls, returns ONLY the predictions of the postive class (1) probability in an ARRAY 