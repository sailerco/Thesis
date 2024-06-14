import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pandas as pd
from matplotlib import pyplot as plt
from transformers import pipeline

import CsvConverter as conv
import seaborn as sns
import torch

"""
ZSC + NLI to match user stories to skills 
"""

name = 'deberta_withHypo'
url = "ClassifierOutput/" + name
# loads ZSC from huggingface
bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
deberta_large ="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
sileod = 'sileod/deberta-v3-base-tasksource-nli'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
classifier = pipeline('zero-shot-classification', device=device, model=deberta_base)

user_stories = pd.read_csv('userStories.csv', delimiter=';')
user_stories.columns = ['user_stories', 'skills']
user_stories = user_stories['user_stories'].tolist()

# loads skills and components from prepared csv files
df = pd.read_csv('D:/Thesis/DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
labels = df[0].tolist()

hypothesis_template = "To resolve this issue the skill {} is needed."


# do the classification
results = classifier(user_stories, labels, multi_label=True, hypothesis_template=hypothesis_template)

with open(url + ".txt", 'w') as f:
    for story, result in zip(user_stories, results):
        f.write(f"Story: {story}\n")
        for label, score in zip(result['labels'], result['scores']):
            f.write(f"- {label}: {score:.2f}\n")
print("Done")

csv = conv.CsvConverter(f'D:/Thesis/DB_GroundTruth/{url}.txt', f'D:/Thesis/DB_GroundTruth/{url}.csv', 'Story')
csv.convert()
"""
def create(title, name, url):
    # Load data from CSV
    data = pd.read_csv(url + '.csv', header=0, index_col=0,
                       encoding='ISO-8859-1')  # Update with your file path
    plt.figure(figsize=(40, 40))
    heatmap = sns.heatmap(data, cmap='Blues', annot=False)
    plt.title(title)
    plt.savefig('heatmaps/heatmap_' + name + '.png')

create(name, name, url)"""