import pandas as pd
from transformers import pipeline

import CsvConverter as conv

"""
ZSC + NLI to match user stories to skills 
"""

# loads ZSC from huggingface
bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
deberta_large ="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
sileod = 'sileod/deberta-v3-base-tasksource-nli'
classifier = pipeline('zero-shot-classification', model=bart)

user_stories = pd.read_csv('userStories.csv', delimiter=';')
user_stories.columns = ['user_stories', 'skills']
user_stories = user_stories['user_stories'].tolist()

# loads skills and components from prepared csv files
df = pd.read_csv('D:/Thesis/DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
labels = df[0].tolist()

# do the classification
results = classifier(user_stories, labels, multi_label=False)

with open('ClassifierOutput/bart_NOT_multi.txt', 'w') as f:
    for story, result in zip(user_stories, results):
        f.write(f"Story: {story}\n")
        for label, score in zip(result['labels'], result['scores']):
            f.write(f"- {label}: {score:.2f}\n")
print("Done")

csv = conv.CsvConverter('D:/Thesis/DB_GroundTruth/ClassifierOutput/bart.txt', 'D:/Thesis/DB_GroundTruth/ClassifierOutput/bart_filtered_wow.csv', 'Story')
csv.convert()