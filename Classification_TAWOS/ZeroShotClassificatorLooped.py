import gc
import torch
from timeit import default_timer as timer
import ray
import pandas as pd
from transformers import pipeline
import csv

"""
    ZSC with a hard coded loop to avoid out of memory
"""

torch.cuda.empty_cache()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

TASK = "grouped"
name = f"deberta_{TASK}"
PATH_NAME = 'final_assets'
read_url = f"{PATH_NAME}/output_txt/{name}.txt"
save_url = f"{PATH_NAME}/output_csv/{name}.csv"
keyword = 'Story'

bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"


def get_sequence(url, columns, column):
    sequence = pd.read_csv(url, delimiter=None, sep=None)
    sequence.columns = columns
    return sequence[column].tolist()


def get_labels(url, delimiter):
    df = pd.read_csv(url, header=None, encoding='ISO-8859-1', delimiter=delimiter)
    return df[0].tolist()


def classification():
    # loads ZSC from huggingface
    classifier = pipeline('zero-shot-classification', device=device, model=deberta_base)

    premise = get_sequence(f'final_assets/UserStoriesWithComponents_{TASK}-8000.csv',
                           ['ID', 'Description', 'Type', 'Component_Names'], 'Description')

    print(f"length of seq before {len(premise)}")
    hypothesis_labels = get_labels(f'final_assets/{TASK}-8000_comps.csv', ';')
    start = timer()

    # do the classification
    batch_size = 20
    results = []
    for i in range(0, len(premise), batch_size):
        result = classifier(premise[i:i + batch_size], hypothesis_labels, multi_label=True)
        results += result
        print(f"{i} - {timer()}")
        del result
        torch.cuda.empty_cache()
        gc.collect()
    end = timer()
    print(end - start)
    print("Done")
    print(results)
    return results, premise


results, user_stories = classification()

with open('final_assets/output_txt/' + name + '.txt', 'w', encoding='utf-8') as f:
    for story, result in zip(user_stories, results):
        f.write(f"Story: {story}\n")
        for label, score in zip(result['labels'], result['scores']):
            f.write(f"- {label}: {score:.2f}\n")

with open(read_url, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# dictonary, data is going to be saved to
data = {}
skill = None
for line in lines:
    if line.strip():
        if line.startswith(keyword):
            key, value = line.replace("\n", "").split(': ', 1)
            skill = value
            data[skill] = {}
        else:
            key, value = line.replace("\n", "").rsplit(': ', 1)
            component, weight = key.replace("- ", "", 1), float(value)
            data[skill][component] = weight

# convert to a better format
output_data = {}
for skill, components in data.items():
    for component, weight in components.items():
        if component not in output_data:
            output_data[component] = {}
        output_data[component][skill] = weight

# saving the file
with open(save_url, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    cleaned_headers = [header.strip().strip('"') for header in list(data.keys())]
    cleaned_headers.insert(0, 'Skills')
    writer.writerow(cleaned_headers)
    for component, values in output_data.items():
        row = [component] + [values.get(skill, '') for skill in data.keys()]
        writer.writerow(row)

# Read the CSV file into a DataFrame and sort it
df = pd.read_csv(save_url, encoding='ISO-8859-1')
df_sorted = df.sort_values(by='Skills')
df_sorted.to_csv(save_url, index=False)
