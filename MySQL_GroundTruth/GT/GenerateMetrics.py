import numpy as np
import pandas as pd
from sklearn import metrics
from tabulate import tabulate

# threshold = 0.95
avg = 'macro'

thresholds = [1.0, 0.95, 0.9, 0.8, 0.5]
# header = ['Threshold', 'Label Density', 'Subset Accuracy', 'ROC over AUC WITHOUT t', 'ROC AUC', 'Precision', 'Recall', 'F1 Score', 'F-Beta Score', 'Avg Precision', 'Hamming Loss', 'Jaccard Loss']
# header = ['Threshold', 'Label Density', 'Subset Accuracy', 'ROC over AUC WITHOUT t', 'ROC AUC', 'Recall', 'F1 Score', 'F-Beta Score', 'Avg Precision', 'Hamming Loss', 'Jaccard Loss']
header = ['Threshold', 'Label Density', 'Subset Accuracy', 'Recall', 'F1 Score', 'F-Beta Score', 'Hamming Loss',
          'ROC AUC', 'Jaccard Loss']


def calculate_label_density(predictions):
    label_cardinality = np.sum(predictions, axis=0)
    label_density = np.mean(label_cardinality)
    return label_density


def getMetricsValues(ground_truth, zsc, zsc_th, threshold):
    metrics_value = [
        round(threshold, 4),
        round(calculate_label_density(zsc_th), 2),
        round(metrics.accuracy_score(ground_truth, zsc_th), 4),  # -> hohe Werte besser
        round(metrics.recall_score(ground_truth, zsc_th, average=avg), 4),
        round(metrics.f1_score(ground_truth, zsc_th, average=avg), 4),  # -> hohe Werte besser
        round(metrics.fbeta_score(ground_truth, zsc_th, beta=1.5, average=avg), 4),
        round(metrics.hamming_loss(ground_truth, zsc_th), 4),  # -> niedrige Werte besser
        round(metrics.roc_auc_score(ground_truth, zsc_th), 4),
        round(metrics.jaccard_score(ground_truth, zsc_th, average=avg), 4)
    ]

    return metrics_value


def get_metrics(name, file):
    ground_truth = pd.read_csv(f'truth{file}.csv', header=None, skiprows=[0], index_col=None).drop(columns=0)
    for col in ground_truth.columns:
        ground_truth[col] = ground_truth[col].fillna(0)

    zsc = (pd.read_csv(f'../final_assets/Output/{name}{file}.csv', header=None, skiprows=[0], index_col=None)
           .drop(columns=0))
    table = []
    for threshold in thresholds:
        zsc_th = zsc.applymap(lambda x: 1 if x >= threshold else 0)
        values = getMetricsValues(ground_truth, zsc, zsc_th, threshold)
        table.append(values)
    print(tabulate(table, headers=header))


for i in ["_removed", "_grouped", "_removed_grouped"]:
    print(f"---{i}---")
    print("---BART---")
    get_metrics("bart", i)
    print("\n---DEBERTA---")
    get_metrics("deberta", i)


"""    metrics_value = [
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
]"""
