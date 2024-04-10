import pandas as pd
from transformers import pipeline

# Wähle das zero-shot-classification Modell
classifier = pipeline('zero-shot-classification', model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli") #model="facebook/bart-large-mnli") #MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli

df = pd.read_csv('D:/Thesis/DB/datasets/skills.csv', header=None)
labels = df[0].tolist()
print(labels)
df_skills = pd.read_csv('DataFromDB/component.csv', header=None, encoding='ISO-8859-1')
skills = df_skills[0].tolist()

print(skills)

# Führe die Klassifizierung durch
results = classifier(skills, labels, multi_label=True)

with open('ClassifierOutput/skills_classification_large-mnli-fever-anli-ling-wanli.txt', 'w') as f:
    for skill, result in zip(skills, results):
        f.write(f"Skill: {skill}\n")
        print(f"Skill: {skill}")
        for label, score in zip(result['labels'], result['scores']):
            f.write(f"- {label}: {score:.2f}\n")
            print(f"- {label}: {score:.2f}")