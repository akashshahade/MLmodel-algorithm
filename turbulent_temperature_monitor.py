
import numpy as np
import pandas as pd

def turbulent_temp_monitor(temp_series, time_step_min=5, window_readings=12):
    df = pd.DataFrame({'Temperature': temp_series})
    df['RollingMean'] = df['Temperature'].rolling(window=window_readings, min_periods=1).mean()
    df['RollingMax'] = df['Temperature'].rolling(window=window_readings, min_periods=1).max()
    df['RollingMin'] = df['Temperature'].rolling(window=window_readings, min_periods=1).min()

    df['DeltaUpper'] = df['RollingMax'] - df['RollingMean']
    df['DeltaLower'] = df['RollingMean'] - df['RollingMin']

    df['DeltaT'] = np.gradient(df['Temperature'].fillna(0))
    df['Delta2T'] = np.gradient(df['DeltaT'])

    df['Alert'] = 'Normal'
    for i in range(len(df)):
        T = df.loc[i, 'Temperature']
        dT = df.loc[i, 'DeltaT']
        d2T = df.loc[i, 'Delta2T']
        du = df.loc[i, 'DeltaUpper']
        dl = df.loc[i, 'DeltaLower']

        if pd.isna(T) or T == 0:
            df.at[i, 'Alert'] = 'Invalid Sensor'
        elif abs(d2T) > 0.75 and abs(dT) > 0.5:
            df.at[i, 'Alert'] = 'Spike Alert'
        elif abs(dT) > 0.5 and du > 3:
            df.at[i, 'Alert'] = 'Critical Rising'
        elif 1.5 <= du <= 3 or 1.5 <= dl <= 3:
            df.at[i, 'Alert'] = 'Warning'

    return df
