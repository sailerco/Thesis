import pandas as pd
from sklearn import metrics
import numpy as np

threshold = 0.9
avg = 'macro'

def calculate_label_density(predictions):
    label_cardinality = np.sum(predictions, axis=0)
    label_density = np.mean(label_cardinality)
    return label_density

def get_metrics(name):
    ground_truth = pd.read_csv('truth.csv', header=None, skiprows=[0], index_col=None).drop(columns=0)
    for col in ground_truth.columns:
        ground_truth[col] = ground_truth[col].fillna(0)

    zsc = (pd.read_csv(f'../ClassifierOutput/{name}.csv', header=None, skiprows=[0], index_col=None)
           .drop(columns=0))
    zsc_th = zsc.applymap(lambda x: 1 if x >= threshold else 0)
    print(f"Label Density: {round(calculate_label_density(zsc_th), 2)}")
    metrics_dict = {
        "Threshold": round(threshold, 4),
        "Subset Accuracy": round(metrics.accuracy_score(ground_truth, zsc_th), 4),  # -> hohe Werte besser
        "ROC over AUC WITHOUT t": round(metrics.roc_auc_score(ground_truth, zsc), 4),
        "ROC AUC": round(metrics.roc_auc_score(ground_truth, zsc_th), 4),
        "Precision": round(metrics.precision_score(ground_truth, zsc_th, average=avg), 4),
        "Recall": round(metrics.recall_score(ground_truth, zsc_th, average=avg), 4),
        "F1 Score": round(metrics.f1_score(ground_truth, zsc_th, average=avg), 4),  # -> hohe Werte besser
        "F-Beta Score": round(metrics.fbeta_score(ground_truth, zsc_th, beta=1.5, average=avg), 4),
        "Avg Precision": round(metrics.average_precision_score(ground_truth, zsc_th, average=avg), 4),
        "Hamming Loss": round(metrics.hamming_loss(ground_truth, zsc_th), 4),  # -> niedrige Werte besser
        "Jaccard Loss": round(metrics.jaccard_score(ground_truth, zsc_th, average=avg), 4)  # -> niedrige Werte besser
    }

    # Print the metrics
    for metric, value in metrics_dict.items():
        print(f"{metric}: {value}")


print("---BART---")
get_metrics("bart")
print("\n---DEBERTA---")
get_metrics("deberta_base")

