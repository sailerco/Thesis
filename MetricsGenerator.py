import os
import CsvConverter as Conv
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.preprocessing import binarize
from tabulate import tabulate


def read_file(path):
    #    csv = pd.read_csv(path, header=None, index_col=None, usecols=[1,2], skiprows=[0])
    csv = pd.read_csv(path, header=None, index_col=None, skiprows=[0]).drop(columns=0)
    return csv


def calculate_label_density(predictions):
    label_cardinality = np.sum(predictions, axis=1)
    label_density = np.mean(label_cardinality)
    return label_density


def set_truth(name, truth_dir):
    return f'truth{name}.csv' if truth_dir else 'truth.csv'


class MetricsGenerator:
    header = ['Threshold', 'Label Density', 'Subset Accuracy', 'Recall', 'F1 Score', 'F-Beta Score', 'Hamming Loss', "ROC AUC", "Jaccard Loss"]
    avg = 'macro'
    truth = None

    thresholds = [1.0, 0.95, 0.9, 0.8, 0.5]
    file_dir = os.getcwd()
    file_dir = os.path.dirname(file_dir)
    if file_dir.endswith("Synth"):
        file_dir = os.path.dirname(file_dir)
    BART_METRICS = os.path.join(file_dir, "Classification_Synth", "GT", "metrics", "bart_metrics.csv")
    DEBERTA_METRICS = os.path.join(file_dir, "Classification_Synth", "GT", "metrics", "deberta_metrics.csv")
    compareBart = None

    def __init__(self, name, file_dir, end_dir, truth_dir, bart, deberta):
        self.bart = bart
        self.deberta = deberta
        self.truth_dir = truth_dir
        self.name = name
        self.file_dir = file_dir
        self.end_dir = end_dir

    def get_metrics_values(self, ground_truth, prediction, threshold):
        ground_truth = ground_truth.to_numpy()
        prediction = prediction.to_numpy()
        metrics_value = [
            round(threshold, 4),
            round(calculate_label_density(prediction.T), 2),
            round(metrics.accuracy_score(ground_truth.T, prediction.T), 4),  # -> hohe Werte besser
            round(metrics.recall_score(ground_truth, prediction, average=self.avg), 4),
            round(metrics.f1_score(ground_truth, prediction, average=self.avg), 4),  # -> hohe Werte besser
            round(metrics.fbeta_score(ground_truth, prediction, beta=2, average=self.avg), 4),
            round(metrics.hamming_loss(ground_truth, prediction), 4),  # -> niedrige Werte besser
            round(metrics.roc_auc_score(ground_truth, prediction), 4),
            round(metrics.jaccard_score(ground_truth, prediction, average=self.avg), 4)
        ]

        return metrics_value

    def compare(self, df):
        if self.compareBart:
            old = pd.read_csv(self.BART_METRICS)
        else:
            old = pd.read_csv(self.DEBERTA_METRICS)
        differences = df - old
        print("Differences:")
        print(tabulate(differences, headers=self.header, showindex=False))

    def get_files(self, file):
        # read the truth and prediction
        ground_truth = read_file(os.path.join(self.file_dir, self.truth))
        prediction = read_file(os.path.join(self.end_dir, f'{file}{self.name}.csv'))

        for col in ground_truth.columns:
            ground_truth[col] = ground_truth[col].fillna(0.0)

        return ground_truth, prediction

    def get_metrics(self, file):
        ground_truth, prediction = self.get_files(file)
        # set threshold and create metrics
        table = []
        for threshold in self.thresholds:
            threshold_prediction = prediction.applymap(lambda x: 1 if x >= threshold else 0)
            values = self.get_metrics_values(ground_truth, threshold_prediction, threshold)
            table.append(values)
        print(tabulate(table, headers=self.header))

        # compare with original metric
        df = pd.DataFrame(table, columns=self.header)
        self.compare(df)

    def main(self):
        print(f"---{self.name}---")

        self.truth = set_truth(self.name, self.truth_dir)

        if self.bart:
            print("---BART---")
            self.compareBart = True
            self.get_metrics("bart")
        if self.deberta:
            self.compareBart = False
            print("\n---DEBERTA---")
            self.get_metrics("deberta")
