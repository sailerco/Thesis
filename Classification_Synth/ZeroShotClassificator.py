import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import pandas as pd
from transformers import pipeline
import CsvConverter as conv
import torch

"""
    ZSC + NLI to match user stories to skills 
"""

name = 'deberta'
url = "ClassifierOutput/" + name

# loads ZSC from huggingface
bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"

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

csv = conv.CsvConverter(f'D:/Thesis/Classification_Synth/{url}.txt', f'D:/Thesis/DB_GroundTruth/{url}.csv', 'Story')
csv.convert()