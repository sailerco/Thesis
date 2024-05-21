import numpy as np
import pandas as pd
from sklearn import metrics
from tabulate import tabulate

#threshold = 0.95
avg = 'macro'
thresholds = [1.0, 0.95, 0.9, 0.8, 0.5]
#header = ['Threshold', 'Label Density', 'Subset Accuracy', 'ROC over AUC WITHOUT t', 'ROC AUC', 'Precision', 'Recall', 'F1 Score', 'F-Beta Score', 'Avg Precision', 'Hamming Loss', 'Jaccard Loss']
header = ['Threshold', 'Label Density', 'Subset Accuracy', 'ROC over AUC WITHOUT t', 'ROC AUC', 'Recall', 'F1 Score', 'F-Beta Score', 'Avg Precision', 'Hamming Loss', 'Jaccard Loss']
def calculate_label_density(predictions):
    label_cardinality = predictions.sum(axis=0)
    label_density = np.mean(label_cardinality)
    return label_density


def getMetricsValues(ground_truth, zsc, zsc_th, threshold):
    metrics_value = [
        round(threshold, 4),
        round(calculate_label_density(zsc_th), 2),
        round(metrics.accuracy_score(ground_truth, zsc_th), 4),  # -> hohe Werte besser
        round(metrics.roc_auc_score(ground_truth, zsc), 4),
        round(metrics.roc_auc_score(ground_truth, zsc_th), 4),
        #round(metrics.precision_score(ground_truth, zsc_th, average=avg), 4),
        round(metrics.recall_score(ground_truth, zsc_th, average=avg), 4),
        round(metrics.f1_score(ground_truth, zsc_th, average=avg), 4),  # -> hohe Werte besser
        round(metrics.fbeta_score(ground_truth, zsc_th, beta=1.5, average=avg), 4),
        round(metrics.average_precision_score(ground_truth, zsc_th, average=avg), 4),
        round(metrics.hamming_loss(ground_truth, zsc_th), 4),  # -> niedrige Werte besser
        round(metrics.jaccard_score(ground_truth, zsc_th, average=avg), 4)
    ]
    return metrics_value

def printMetrics(values):
    metrics_dict = {
        "Threshold": values[0],
        "Label Density": values[1],
        "Subset Accuracy": values[2],  # -> hohe Werte besser
        "ROC over AUC WITHOUT t": values[3],
        "ROC AUC": values[4],
        "Precision": values[5],
        "Recall": values[6],
        "F1 Score": values[7],  # -> hohe Werte besser
        "F-Beta Score": values[8],
        "Avg Precision": values[9],
        "Hamming Loss": values[10],  # -> niedrige Werte besser
        "Jaccard Loss": values[11] # -> niedrige Werte besser
    }
    # Print the metrics
    for metric, value in metrics_dict.items():
        print(f"{metric}: {value}")


def get_metrics(name):
    ground_truth = pd.read_csv('truth.csv', usecols=[1], header=None, skiprows=[0], index_col=None)#.drop(columns=0)
    for col in ground_truth.columns:
        ground_truth[col] = ground_truth[col].fillna(0)
    zsc = pd.read_csv(f'../ClassifierOutput/{name}.csv', usecols=[1], header=None, skiprows=[0], index_col=None)
           #.drop(columns=0))
    table = []
    for threshold in thresholds:
        zsc_th = zsc.applymap(lambda x: 1 if x >= threshold else 0)
        values = getMetricsValues(ground_truth, zsc, zsc_th, threshold)
        table.append(values)
        #printMetrics(values)
    print(tabulate(table, headers=header, tablefmt="pretty"))


print("---BART---")
get_metrics("bart")
print("\n---DEBERTA---")
get_metrics("deberta_base")