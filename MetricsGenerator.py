import os

import numpy as np
import pandas as pd
from sklearn import metrics
from tabulate import tabulate


class MetricsGenerator:
    def __init__(self, name, dir, end_dir):
        self.name = name
        self.dir = dir
        self.end_dir = end_dir
        self.header = ['Threshold', 'Label Density', 'Subset Accuracy', 'Recall', 'F1 Score', 'F-Beta Score',
                       'Hamming Loss',
                       'ROC AUC', 'Jaccard Loss']
        self.avg = 'macro'
        self.thresholds = [1.0, 0.95, 0.9, 0.8, 0.5]

    def calculate_label_density(self, predictions):
        label_cardinality = np.sum(predictions, axis=0)
        label_density = np.mean(label_cardinality)
        return label_density

    def getMetricsValues(self, ground_truth, zsc, zsc_th, threshold):
        metrics_value = [
            round(threshold, 4),
            round(self.calculate_label_density(zsc_th), 2),
            round(metrics.accuracy_score(ground_truth, zsc_th), 4),  # -> hohe Werte besser
            round(metrics.recall_score(ground_truth, zsc_th, average=self.avg), 4),
            round(metrics.f1_score(ground_truth, zsc_th, average=self.avg), 4),  # -> hohe Werte besser
            round(metrics.fbeta_score(ground_truth, zsc_th, beta=1.5, average=self.avg), 4),
            round(metrics.hamming_loss(ground_truth, zsc_th), 4),  # -> niedrige Werte besser
            round(metrics.roc_auc_score(ground_truth, zsc_th), 4),
            round(metrics.jaccard_score(ground_truth, zsc_th, average=self.avg), 4)
        ]

        return metrics_value

    def get_metrics(self, name, file):
        ground_truth = pd.read_csv(os.path.join(self.dir, f'truth{file}.csv'), header=None, skiprows=[0], index_col=None).drop(columns=0)
        for col in ground_truth.columns:
            ground_truth[col] = ground_truth[col].fillna(0)

        zsc = (pd.read_csv(os.path.join(self.end_dir, f'{name}{file}.csv'), header=None, skiprows=[0], index_col=None)
               .drop(columns=0))
        table = []
        for threshold in self.thresholds:
            zsc_th = zsc.applymap(lambda x: 1 if x >= threshold else 0)
            values = self.getMetricsValues(ground_truth, zsc, zsc_th, threshold)
            table.append(values)
        print(tabulate(table, headers=self.header))

    def main(self):
        print(f"---{self.name}---")
        print("---BART---")
        self.get_metrics("bart", self.name)
        print("\n---DEBERTA---")
        self.get_metrics("deberta", self.name)
