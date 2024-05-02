import pandas as pd
from sklearn.metrics import accuracy_score

def compute_accuracy(gt, zsc):
    matching_values = (gt == zsc).sum().sum()  # Number of matching values
    accuracy = (matching_values / zsc.size) * 100  # Calculate accuracy percentage
    print(accuracy)


def compute_accuracy_sklearn(gt, zsc):
    gt = gt.values.ravel()
    zsc = zsc.values.ravel()
    accuracy = accuracy_score(gt, zsc)
    print(accuracy)


threshold = 0.9
df = pd.read_csv('truth.csv')
columns = df.columns
df1 = pd.read_csv('truth.csv', header=None, skiprows=[0], index_col=None).drop(columns=0)

for col in df1.columns:
    df1[col] = df1[col].fillna(0)

df2 = (pd.read_csv('../ClassifierOutput/bart.csv', header=None, skiprows=[0], index_col=None)
       .drop(columns=0)
       .applymap(lambda x: 1 if x >= threshold else 0))

compute_accuracy(df1, df2)
compute_accuracy_sklearn(df1, df2)

