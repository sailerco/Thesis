import numpy as np
import pandas as pd
from sklearn import metrics

"""
    Calculate the JACCARD Score between two given sets. Additionally calculate the label density
"""
FIRST_PATH = "PreFineTuning/bart_all_labels.csv"
SECOND_PATH = "PostFineTuning/bart_all_labels_10Eps.csv"
PATH_LABEL_DENSITY = "PostFineTuning/bart_all_labels_10Eps.csv"

threshold = [1.0, 0.9, 0.8, 0.7]
first_prediction_set = pd.read_csv(FIRST_PATH, header=None, index_col=None, skiprows=[0]).drop(columns=0)

second_prediction_set = pd.read_csv(SECOND_PATH, header=None, index_col=None, skiprows=[0]).drop(columns=0)

for i in threshold:
    before_df_th = first_prediction_set.applymap(lambda x: 1 if x >= i else 0)
    after_df_th = second_prediction_set.applymap(lambda x: 1 if x >= i else 0)
    jaccard_score_result = round(metrics.jaccard_score(before_df_th, after_df_th, average="macro"), 4)
    print(f"{i}: {jaccard_score_result}")


def calculate_label_density(predictions):
    label_cardinality = np.sum(predictions, axis=0)
    label_density = np.mean(label_cardinality)
    return label_density


zsc = pd.read_csv(PATH_LABEL_DENSITY, header=None, skiprows=[0], index_col=None).drop(columns=0)
zsc_th = zsc.applymap(lambda x: 1 if x >= 0.7 else 0)
print(calculate_label_density(zsc_th))
