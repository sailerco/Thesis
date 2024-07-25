import numpy as np
from sklearn import metrics
import pandas as pd
import sklearn.metrics

"""
    get the jaccard score
"""
threshold = [1.0, 0.9, 0.8, 0.7]
before_df = pd.read_csv("PreFineTuning/deberta_all_labels.csv", header=None, index_col=None, skiprows=[0]).drop(
    columns=0)

after_df = pd.read_csv("PostFineTuning/deberta_all_labels.csv", header=None, index_col=None, skiprows=[0]).drop(
    columns=0)

for i in threshold:
    before_df_th = before_df.applymap(lambda x: 1 if x >= i else 0)
    after_df_th = after_df.applymap(lambda x: 1 if x >= i else 0)
    jaccard = round(metrics.jaccard_score(before_df_th, after_df_th, average="micro"), 4)
    print(f"mean: {sklearn.metrics.mean_absolute_error(before_df_th, after_df_th)}")
    print(jaccard)

def calculate_label_density(predictions):
    label_cardinality = np.sum(predictions, axis=0)
    label_density = np.mean(label_cardinality)
    return label_density


zsc = pd.read_csv("PostFineTuning/bart_all_labels.csv", header=None, skiprows=[0], index_col=None).drop(columns=0)
zsc_th = zsc.applymap(lambda x: 1 if x >= 0.7 else 0)
print(calculate_label_density(zsc_th))
