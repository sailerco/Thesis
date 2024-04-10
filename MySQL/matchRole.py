import pandas as pd
from transformers import pipeline

# Wähle das zero-shot-classification Modell
classifier = pipeline('zero-shot-classification', model="facebook/bart-large-mnli") #model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli") #MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli

df = pd.read_csv('D:/Thesis/DB/datasets/Roles_small.csv', header=None, skiprows=1)
roles_labels = df[0].tolist()
print(roles_labels)
#df_userWithComponents = pd.read_csv('UserComponents.csv', header=None, encoding='ISO-8859-1')
#user_comp = df_userWithComponents[0].tolist()
#user_comp = ["User #71 has worked with components: Stream Module, Batch, Documentation, Packaging, Runtime, Configuration, Hadoop, Ingest, Acceptance Testing, CLI"]
user_comp = ["User 257 has components: Infrastructure (127), Core (75), Repository (23), Kotlin (7), Mapping (56), Configuration (24), SessionFactory (10), Template API (19), Documentation (29), API (1), Cassandra Administration (5)"]
print(user_comp)

# Führe die Klassifizierung durch
results = classifier(user_comp, roles_labels, multi_label=True)

#with open('skills_classification_large-mnli-fever-anli-ling-wanli.txt', 'w') as f:
for comp, result in zip(user_comp, results):
    #f.write(f"User: {comp}\n")
    print(f"User: {comp}")
    for label, score in zip(result['labels'], result['scores']):
        #f.write(f"- {label}: {score:.2f}\n")
        print(f"- {label}: {score:.2f}")