import os

import pandas as pd
import torch
from transformers import pipeline

import CsvConverter as conv

"""
    Zero Shot Classification between TAWOS user stories (assets/jira.csv) and synth skills; usage of fine tuned models. 
"""


bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
deberta_path = "../FineTuning/FinalRuns_PreTrained/deberta_6_2e-05_3232_0.1_0.06"
bart_path = "../FineTuning/FinalRuns_PreTrained/6_1e-05_3232_0.1_0.06"

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def compute(ft, model):
    if ft:
        directory = "PostFineTuning"
        if model == "bart":
            classifier = pipeline('zero-shot-classification', device=device, model=bart_path)
        else:
            classifier = pipeline('zero-shot-classification', device=device, model=deberta_path)
    else:
        directory = "PreFineTuning"
        if model == "bart":
            classifier = pipeline('zero-shot-classification', device=device, model=bart)
        else:
            classifier = pipeline('zero-shot-classification', device=device, model=deberta_base)

    user_stories = pd.read_csv('assets/jira.csv', delimiter=None, sep=None, encoding='utf-8')
    user_stories = user_stories['Description'].tolist()

    # loads skills and components from prepared csv files
    df = pd.read_csv('../DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
    labels = df[0].tolist()

    results = classifier(user_stories, labels, multi_label=True)

    name = "all_labels2_"
    with open(f"{directory}/{model}_{name}.txt", 'w') as f:
        for story, result in zip(user_stories, results):
            print(story, result)
            f.write(f"Story: {story}\n")
            for label, score in zip(result['labels'], result['scores']):
                f.write(f"- {label}: {score:.2f}\n")
    print("Done")

    dir = os.getcwd()
    csv = conv.CsvConverter(os.path.join(dir, directory, f'{model}_{name}.txt'),
                            os.path.join(dir, directory, f'{model}_{name}.csv'), 'Story')
    csv.convert()


compute(True, "bart")
compute(True, "deberta")
compute(False, "bart")
compute(False, "deberta")