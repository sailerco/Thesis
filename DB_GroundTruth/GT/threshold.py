import pandas as pd
threshold = 0.9
#extract the csv of a threshold
zsc_1 = pd.read_csv(f'../ClassifierOutput/bart.csv')
columns = zsc_1.columns[1:3]
print(columns)
row_headers = zsc_1.iloc[:, 0]
zsc = pd.read_csv(f'../ClassifierOutput/bart.csv', usecols=[1,2], header=None, skiprows=[0], index_col=None)
       #.drop(columns=0))
zsc_th = zsc.applymap(lambda x: 1 if x >= threshold else 0)
zsc_th.columns = columns
zsc_th.index = row_headers
zsc_th.to_csv('threshold_09_2.csv', header=True, index=True)