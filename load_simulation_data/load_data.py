import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd
from datetime import datetime
import seaborn as sns

# periods
periods_var = 31 + 28 + 31  # Für die ersten drei Monate

# Number of Time series

for k in range(2, 10):       # Anpassung für die weiteren Dateien
    # set an empty dataframe
    df_ts = pd.DataFrame(columns=['datetime', 'pulse', 'category', 'ts_number'])

    # Anzahl der "Probanden" pro .csv
    ts_count = 500
    for i in range(1, ts_count + 1):
        # Random selection for mean and standard deviation from a normal distribution for different pulse levels
        mu_pulse_low = np.random.normal(50, 3, 1)
        sigma_pulse_low = abs(np.random.normal(1, 2, 1))

        mu_pulse_mid = np.random.normal(65, 5, 1)
        sigma_pulse_mid = abs(np.random.normal(1, 2, 1))

        mu_pulse_high = np.random.normal(80, 5, 1)
        sigma_pulse_high = abs(np.random.normal(1, 2, 1))

        # Create a list from above random selection for each athlete level
        select_list = [[mu_pulse_low, sigma_pulse_low, 'pro_athlete'],
                       [mu_pulse_mid, sigma_pulse_mid, 'athlete'],
                       [mu_pulse_high, sigma_pulse_high, 'non_athlete']]

        # select a uniform random choice from above list
        random_selection = np.random.randint(low=0, high=3, size=1, dtype=int)[0]
        print(i)
        # Loop through each time series for daily (random) pulse observation
        for time, pulse in zip(pd.date_range("2021-01-01", periods=periods_var, freq="D"),
                               np.random.normal(select_list[random_selection][0], select_list[random_selection][1],
                                                periods_var)):
            df_temp = pd.DataFrame([[datetime.date(time), round(float(pulse), 0), select_list[random_selection][2],
                                     str(k) + '_' + str(i)]], columns=['datetime', 'pulse', 'category', 'ts_number'])
            df_ts = df_ts.append(df_temp)

            df_ts.to_csv(f"ts_data_{k}.csv", index=False)
            df_ts


# Zusatz Code für Time Series plot und classification
"""
# Time series plot
sns.lineplot(x="datetime", y="pulse",
             hue="ts_number",
             data=df_ts.head(periods_var * 5))  # show the first 5 time series for the first three months

#Data Frame classification
df_classification = df_ts.groupby(['ts_number', 'category']).describe()
"""