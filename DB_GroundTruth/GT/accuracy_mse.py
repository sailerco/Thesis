import pandas as pd
from sklearn.metrics import root_mean_squared_error
import numpy as np

df1 = pd.read_csv('truth.csv', header=None, skiprows=[0], index_col=None)
df1 = df1.drop(columns=0)

for col in df1.columns:
    df1[col] = df1[col].fillna(0)
df2 = pd.read_csv('../ClassifierOutput/bart.csv', header=None, skiprows=[0], index_col=None)
df2 = df2.drop(columns=0)

mse = root_mean_squared_error(df1, df2)
print(mse)