import numpy as np
import pandas as pd
from datetime import datetime


# Simulate daily data for three month, starting from 1st January 2021.
periods_var = 31 + 28 + 31

# Data Simulation using random observations from normal distributions
for k in range(1, 50):    # Choose the range for creating csv files. Each iteration creates a csv file with notation k.
    # set an empty dataframe
    df_ts = pd.DataFrame(columns=['datetime', 'pulse', 'category', 'ts_number'])

    ts_count = 500  # Number of "probands" for each csv datafile.
    for i in range(1, ts_count + 1):
        # Random selection for mean and standard deviation from a normal distribution for different pulse levels.

        # Pulse simulation for 'pro athlete':
        mu_pulse_low = np.random.normal(50, 3, 1)
        sigma_pulse_low = abs(np.random.normal(1, 2, 1))

        # Pulse simulation for 'athlete':
        mu_pulse_mid = np.random.normal(65, 5, 1)
        sigma_pulse_mid = abs(np.random.normal(1, 2, 1))

        # Pulse simulation for 'non athlete':
        mu_pulse_high = np.random.normal(80, 5, 1)
        sigma_pulse_high = abs(np.random.normal(1, 2, 1))

        # Create a list from above random selection for each athlete level
        select_list = [[mu_pulse_low, sigma_pulse_low, 'pro_athlete'],
                       [mu_pulse_mid, sigma_pulse_mid, 'athlete'],
                       [mu_pulse_high, sigma_pulse_high, 'non_athlete']]

        # select a uniform random choice from above list
        random_selection = np.random.randint(low=0, high=3, size=1, dtype=int)[0]

        # Loop through each time series for daily (random) pulse observation
        for time, pulse in zip(pd.date_range("2021-01-01", periods=periods_var, freq="D"),
                               np.random.normal(select_list[random_selection][0], select_list[random_selection][1],
                                                periods_var)):
            df_temp = pd.DataFrame([[datetime.date(time), round(float(pulse), 0), select_list[random_selection][2],
                                     str(k) + '_' + str(i)]], columns=['datetime', 'pulse', 'category', 'ts_number'])
            df_ts = df_ts.append(df_temp)

            df_ts.to_csv(f"ts_data_{k}.csv", index=False)
            df_ts