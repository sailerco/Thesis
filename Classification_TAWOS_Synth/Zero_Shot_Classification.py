import os

import pandas as pd
import torch
from transformers import pipeline

import CsvConverter as conv

"""
    Zero Shot Classification between TAWOS user stories (assets/jira.csv) and synth skills; usage of fine tuned models. 
"""

BART_BASE = "facebook/bart-large-mnli"
DEBERTA_BASE = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
DEBERTA_FT = "../FineTuning/FinalRuns_PreTrained/deberta_1_08_6_2e-05_3232_0.1_0.06"
BART_FT = "../FineTuning/FinalRuns_PreTrained/bart_08_06_1e-05_3232_0.1_0.06"

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def load_pipeline(ft, model):
    if model == "bart":
        model_path = BART_FT if ft else BART_BASE
    elif model == "deberta":
        model_path = DEBERTA_FT if ft else DEBERTA_BASE

    classifier = pipeline('zero-shot-classification', device=DEVICE, model=model_path)
    return classifier


def load_premises():
    # load the jira.csv, which contains 25 random user stories
    user_stories = pd.read_csv('assets/jira.csv', delimiter=None, sep=None, encoding='utf-8')
    return user_stories['Description'].tolist()


def load_hypothesis():
    # loads skills and components from prepared csv files
    df = pd.read_csv('../DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
    return df[0].tolist()


def save_results_in_txt(results, user_stories, path_name, path_txt):
    path = f"{path_name}/{path_txt}"
    with open(path, 'w') as f:
        for story, result in zip(user_stories, results):
            print(story, result)
            f.write(f"Story: {story}\n")
            for label, score in zip(result['labels'], result['scores']):
                f.write(f"- {label}: {score:.2f}\n")
    print("Done")


def convert_txt_to_csv(path_name, path_txt, path_csv):
    directory = os.getcwd()
    csv = conv.CsvConverter(os.path.join(directory, path_name, path_txt), os.path.join(directory, path_name, path_csv),
                            'Story')
    csv.convert()


def save_results(model, results, user_stories, path_name):
    name = "all_labels_6Eps"
    path_txt = f'{model}_{name}.txt'
    path_csv = f'{model}_{name}.csv'
    save_results_in_txt(results, user_stories, path_name, path_txt)
    convert_txt_to_csv(path_name, path_txt, path_csv)


def compute(ft, model):
    path_name = "PostFineTuning" if ft else "PreFineTuning"
    classifier = load_pipeline(ft, model)
    user_stories = load_premises()
    labels = load_hypothesis()

    results = classifier(user_stories, labels, multi_label=True)
    save_results(model, results, user_stories, path_name)


# compute(True, "bart")
compute(True, "deberta")
# compute(False, "bart")
# compute(False, "deberta")
