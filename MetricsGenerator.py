import os
import CsvConverter as Conv
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.preprocessing import binarize
from tabulate import tabulate


def read_file(path):
    """
    Reads a CSV file and returns the data as a DataFrame.
    Returns:
        pd.DataFrame: The content of the CSV file as a DataFrame, without the header column and row.
    """
    csv = pd.read_csv(path, header=None, index_col=None, skiprows=[0]).drop(columns=0)
    # when using only specific columns, use the following: csv = pd.read_csv(path, header=None, index_col=None, usecols=[1,2], skiprows=[0])
    return csv


def calculate_label_density(predictions):
    """
    Calculates the label density of predictions. The label density is the mean number of labels assigned to the samples.

    Returns:
        float: The mean label density.
    """
    label_cardinality = np.sum(predictions, axis=1)
    label_density = np.mean(label_cardinality)
    return label_density


def set_truth(name, truth_dir):
    """set the truth file path"""
    return f'truth{name}.csv' if truth_dir else 'truth.csv'


class MetricsGenerator:
    """
    A class to generate and compare classification metrics for different models.

    Attributes:
        header (list): Column names for the metrics table.
        header (list): Column names for the metrics table.
        avg (str): The averaging method for calculating metrics (default is 'macro').
        truth (str): The file name of the ground truth data.
        thresholds (list): List of thresholds to apply to the predictions.
        ROOT_DIR (str): The root directory of the project.
        BART_METRICS (str): The file path to the original BART metrics CSV.
        DEBERTA_METRICS (str): The file path to the original DEBERTA metrics CSV.
        compareBart (bool): A flag to determine which model's metrics to compare.
    """

    header = ['Threshold', 'Label Density', 'Subset Accuracy', 'Recall', 'F1 Score', 'F-Beta Score', 'Hamming Loss', "Jaccard Index"]

    avg = 'macro'
    truth = None

    thresholds = [1.0, 0.95, 0.9, 0.8, 0.5]

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
    BART_METRICS = os.path.join(ROOT_DIR, "Classification_Synth", "GroundTruth", "metrics", "bart_metrics.csv")
    DEBERTA_METRICS = os.path.join(ROOT_DIR, "Classification_Synth", "GroundTruth", "metrics", "deberta_metrics.csv")
    compareBart = None

    def __init__(self, name, file_dir, end_dir, truth_dir, bart, deberta):
        """
        Initializes the MetricsGenerator with necessary parameters.

        Args:
            name (str): The (path) name of the model or variant.
            file_dir (str): Directory containing the ground truth files.
            end_dir (str): Directory containing the prediction files.
            truth_dir (bool): Flag indicating whether the truth dir is default or differs
            bart (bool): Flag indicating whether to compute BART metrics.
            deberta (bool): Flag indicating whether to compute DEBERTA metrics.
        """
        self.bart = bart
        self.deberta = deberta
        self.truth_dir = truth_dir
        self.name = name
        self.file_dir = file_dir
        self.end_dir = end_dir

    def get_metrics_values(self, ground_truth, prediction, threshold):
        """
        Computes various metrics between the ground truth and predictions. The metrics include accuracy, recall,
        F1 score, F-Beta score, hamming loss, and jaccard index.

        Args:
            ground_truth (pd.DataFrame): The ground truth data.
            prediction (pd.DataFrame): The predicted data.
            threshold (float): The threshold applied to the predictions.

        Returns:
            list: A list of calculated metric values, including the threshold used.
        """
        ground_truth = ground_truth.to_numpy()
        prediction = prediction.to_numpy()
        metrics_value = [
            round(threshold, 4),
            round(calculate_label_density(prediction.T), 2),
            round(metrics.accuracy_score(ground_truth.T, prediction.T), 4),
            round(metrics.recall_score(ground_truth, prediction, average=self.avg), 4),
            round(metrics.f1_score(ground_truth, prediction, average=self.avg), 4),
            round(metrics.fbeta_score(ground_truth, prediction, beta=2, average=self.avg), 4),
            round(metrics.hamming_loss(ground_truth, prediction), 4),
            round(metrics.jaccard_score(ground_truth, prediction, average=self.avg), 4)
        ]

        return metrics_value

    def compare_with_original_metrics(self, df):
        """
        Compares the calculated metrics with existing BART or DEBERTA metrics
        (default: metrics of first classification without fine-tuned models).
        This method reads the previous metrics from a CSV file and calculates the differences with the current metrics.

        Args:
            df (pd.DataFrame): The DataFrame containing the current metrics.
        """
        if self.compareBart:
            old = pd.read_csv(self.BART_METRICS)
        else:
            old = pd.read_csv(self.DEBERTA_METRICS)
        differences = df - old
        print("Differences:")
        print(tabulate(differences, headers=self.header, showindex=False))

    def get_files(self, file):
        """
        Reads the ground truth and prediction files.
        This method loads the ground truth and prediction data from the respective directories,
        fills missing values in the ground truth data, and returns both datasets.
        """
        ground_truth = read_file(os.path.join(self.file_dir, self.truth))
        prediction = read_file(os.path.join(self.end_dir, f'{file}{self.name}.csv'))

        for col in ground_truth.columns:
            ground_truth[col] = ground_truth[col].fillna(0.0)

        return ground_truth, prediction

    def get_metrics(self, file):
        """
        Calculates metrics for a given prediction file at various thresholds.
        This method calculates metrics for each threshold and compares them with the original metrics.

        Args:
            file (str): The name of the prediction file (e.g., 'bart' or 'deberta').
        """
        ground_truth, prediction = self.get_files(file)

        table = []
        for threshold in self.thresholds:
            threshold_prediction = prediction.applymap(lambda x: 1 if x >= threshold else 0)
            values = self.get_metrics_values(ground_truth, threshold_prediction, threshold)
            table.append(values)

        print(tabulate(table, headers=self.header))

        resulting_metrics = pd.DataFrame(table, columns=self.header)
        self.compare_with_original_metrics(resulting_metrics)

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
