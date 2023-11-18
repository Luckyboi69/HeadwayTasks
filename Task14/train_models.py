import os
import re
import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from feature_extractor_module import FeatureExtractor
# Path to the folder containing train CSV files
train_folder_path = './train_splits/'
# Get a list of all CSV files in the folder
train_files = [file for file in os.listdir(train_folder_path) if file.endswith('.csv')]
feature_extractor = FeatureExtractor()
train_lags_pairs = []
timestamp_intervals=[]
# Function to extract the number from the file name
def extract_number(file_name):
    match = re.search(r'\d+', file_name)
    return int(match.group()) if match else None

# Function to train a model and save it
def train_and_save_model(file_name):
    # Extract the number from the file name
    train_number = extract_number(file_name)
    if train_number is not None:
        # Load the CSV file
        file_path = os.path.join(train_folder_path, file_name)
        dataset = pd.read_csv(file_path)
        df,lags,intervals= feature_extractor.extract_features(dataset,0,0,None)
        y = df['value']
        X= df.drop('value',axis=1)
        model = LinearRegression()
        model.fit(X, y)
        # Save the trained model with the train number in the name
        model_save_path = f'models/model_{train_number}.pkl'
        with open(model_save_path, 'wb') as model_file:
            pickle.dump(model, model_file)
        train_lags_pairs.append((train_number, lags))
        timestamp_intervals.append((train_number,intervals))        

# Loop through each CSV file, train a model, and save it
for train_file in train_files:
    train_and_save_model(train_file)
    print("Model Created Succesfully")
    
df_train_lags = pd.DataFrame(train_lags_pairs, columns=['train_number', 'lags'])
df_train_lags.to_csv('train_lags.csv', index=False)
df_timestamp=pd.DataFrame(timestamp_intervals,columns=['train_number','timestamp_intervals'])
df_timestamp.to_csv('timestamp_intervals.csv',index=False)