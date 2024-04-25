import pandas as pd
from transformers import pipeline

"""
ZSC + NLI to match skills to components 
"""

# loads ZSC from huggingface
bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
deberta_large ="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
sileod = 'sileod/deberta-v3-base-tasksource-nli'
classifier = pipeline('zero-shot-classification', model=deberta_base)

# loads skills and components from prepared csv files
df = pd.read_csv('D:/Thesis/DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
labels = df[0].tolist()
df_skills = pd.read_csv('DataFromDB/component.csv', header=None, encoding='ISO-8859-1')
skills = df_skills[0].tolist()

# do the classification
results = classifier(skills, labels, multi_label=True)

with open('ClassifierOutput/skills_classification_deberta_base.txt', 'w') as f:
    for skill, result in zip(skills, results):
        f.write(f"Skill: {skill}\n")
        print(f"Skill: {skill}")
        for label, score in zip(result['labels'], result['scores']):
            f.write(f"- {label}: {score:.2f}\n")
            print(f"- {label}: {score:.2f}")