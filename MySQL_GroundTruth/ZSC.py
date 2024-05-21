
import torch
from matplotlib import pyplot as plt
from timeit import default_timer as timer

import CsvConverter as conv
import pandas as pd
from transformers import pipeline
import seaborn as sns

"""
ZSC + NLI to match user stories to components 
"""

name = "bart_remain_reduce_task"
url = 'D:/Thesis/MySQL_GroundTruth/ClassifierOutput/' + name

bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
deberta_large = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
sileod = 'sileod/deberta-v3-base-tasksource-nli'

def get_sequence(url, columns, column):
    sequence = pd.read_csv(url, delimiter=None, sep=None)
    sequence.columns = columns
    return sequence[column].tolist()


def get_labels(url, delimiter):
    df = pd.read_csv(url, header=None, encoding='ISO-8859-1', delimiter=delimiter)
    return df[0].tolist()


def classification(name):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # loads ZSC from huggingface
    classifier = pipeline('zero-shot-classification', device=device, model=bart)

    #seq = get_sequence('assets/UserStoriesWithComponents_cleaned_filtered_no_title.csv', ['Type', 'Component_Names', 'TitleAndDescription'], 'TitleAndDescription')
    seq = get_sequence('assets/UserStoriesWithComponents_remain_reduce.csv',
                       ['ID', 'Description', 'Type', 'Component_Names'], 'Description')
    labels = get_labels('assets/components/remain_reduce_comps.csv', ';')
    # do the classification
    start = timer()
    results = classifier(seq, labels, multi_label=True)
    end = timer()
    with open('ClassifierOutput/' + name + '.txt', 'w') as f:
        for story, result in zip(seq, results):
            f.write(f"Story: {story}\n")
            print(story)
            for label, score in zip(result['labels'], result['scores']):
                print(f"- {label}: {score:.2f}")
                f.write(f"- {label}: {score:.2f}\n")
    print(end-start)
    print("Done")


classification(name)

csv = conv.CsvConverter(url + '.txt', url + '.csv', 'Story')
csv.convert()


def create(title, name, url):
    # Load data from CSV
    data = pd.read_csv(url + '.csv', header=0, index_col=0,
                       encoding='ISO-8859-1')  # Update with your file path
    plt.figure(figsize=(40, 40))
    heatmap = sns.heatmap(data, cmap='Blues', annot=False)
    plt.title(title)
    plt.savefig('heatmap/heatmap_' + name + '.png')


create(name, name, url)
