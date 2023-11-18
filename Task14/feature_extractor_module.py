import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import pacf
from prophet import Prophet
class FeatureExtractor:


    def extract_features(self,data,nlags,interval,new_columns):
        correlation_threshold = 0.2
        # Convert the received data into a DataFrame            
        df=pd.DataFrame(data)
        old_column_name='time'
        new_column_name='timestamp'
        if old_column_name in df.columns:
            # Rename the column
            df.rename(columns={old_column_name: new_column_name}, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df=df[['value','timestamp']]

        if interval!=0:
            last_timestamp = df['timestamp'].max()  # Get the last timestamp in the DataFrame
            new_timestamp = last_timestamp + pd.Timedelta(seconds=interval)
            # Create a new row with NaN values for other columns
            new_row = pd.DataFrame([[float('nan')] * len(df.columns)], columns=df.columns)

            # Set the 'timestamp' column of the new row to the calculated timestamp
            new_row['timestamp'] = new_timestamp
            df = pd.concat([df, new_row], ignore_index=True)
            for col in new_columns:
               df[col] = None  # or df[col] = np.nan
            time_features = ['DoW', 'MoY', 'HoD', 'DoM']
            # Add time-related features to df_time if they don't already exist
            for feature in time_features:
                if feature in df.columns:
                    if feature == 'DoW':
                        df[feature] = df['timestamp'].dt.dayofweek
                    elif feature == 'MoY':
                        df[feature] = df['timestamp'].dt.month
                    elif feature == 'HoD':
                        df[feature] = df['timestamp'].dt.hour
                    elif feature == 'DoM':
                        df[feature] = df['timestamp'].dt.day
        else:            
          df_time=df[['value','timestamp']]
          df_time['DoW'] = df['timestamp'].dt.dayofweek  # Day of week (Monday=0, Sunday=6)
          df_time['MoY'] = df['timestamp'].dt.month  # Month of year
          df_time['HoD'] = df['timestamp'].dt.hour  # Hour of day
          df_time['DoM'] = df['timestamp'].dt.day  # Day of month
          df_time.drop(['value','timestamp'],axis=1,inplace=True)
          # Add features with correlation above the threshold to the DataFrame
          for col in df_time:
              correlations = df['value'].corr(df_time[col], method='pearson')
              if abs(correlations) > correlation_threshold:
                  df[col] = df_time[col]
                                    
        # Calculate moving average
        first_timestamp = df['timestamp'].min()
        second_timestamp = df['timestamp'].iloc[1]
        data_interval = (second_timestamp - first_timestamp).total_seconds()
        data_interval=int(data_interval)
        if interval != 0 :
          data_interval=interval
        # Calculate the moving average
        moving_average = df['value'].rolling(data_interval,min_periods=1).mean()
        #if abs(correlations) > correlation_threshold:
        df['moving_average'] = moving_average
        # Add the moving average feature to the DataFrame
        df.ffill(inplace=True)
        if nlags==0:
            
            # Calculate PACF with a reduced number of lags
            pacf_result = pacf(df['value'], nlags=12)

            # Extract significant lags (excluding lag 0)
            threshold = 0.2
            significant_lags = [int(lag) for lag in pacf_result if abs(lag) >= threshold and lag != 1]
            if (len(significant_lags))==0:
             significant_lags.append(1)

            # Add lag features to the DataFrame with correct shifting
            i = 1
            for lag in significant_lags:
                df[f'Lag{i}'] = df['value'].shift(i)
                i += 1
            lagged_features=i-1   
            
            df.dropna(inplace=True)
            
 
        else:
            i=1
            for i in range(1, nlags + 1):
                df[f'Lag{i}'] = df['value'].shift(i)
            lagged_features=0
            
        df_1=df[['timestamp','value']].copy()

        df_1.rename(columns = {'value':'y', 'timestamp':'ds'}, inplace = True)

        # Instantiate the Prophet model
        model = Prophet()

        # Fit the model to the data
        model.fit(df_1)

        # Make future dataframe with only the historical dates
        future = pd.DataFrame(df_1['ds'])

        # Predict the values
        forecast = model.predict(future)
        prophet_features=forecast[['yhat_lower','yhat_upper','trend_lower','trend_upper']].copy()
        # Add features with correlation above the threshold to the DataFrame
        for col in prophet_features:
            correlations = df['value'].corr(prophet_features[col], method='pearson')
            if abs(correlations) > correlation_threshold:
                df[col] = prophet_features[col]
        df.dropna(inplace=True)
        df.set_index('timestamp', inplace=True)
        if lagged_features==0:
            lagged_features=1
    
        return df,lagged_features,data_interval