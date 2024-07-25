import gc
import torch
from timeit import default_timer as timer
import ray
import pandas as pd
from transformers import pipeline
import csv

"""
    ZSC mit RAY um out of memory zu umgehen -> TESTING was besser ist Loop oder Ray. 
"""

# TODO: REFACTORING

torch.cuda.empty_cache()
print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

name = "bart_removed_grouped"
url = 'D:/Thesis/Classification_TAWOS/final_assets/Output/' + name

bart = "facebook/bart-large-mnli"
deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"


def get_sequence(url, columns, column):
    sequence = pd.read_csv(url, delimiter=None, sep=None)
    sequence.columns = columns
    return sequence[column].tolist()


def get_labels(url, delimiter):
    df = pd.read_csv(url, header=None, encoding='ISO-8859-1', delimiter=delimiter)
    return df[0].tolist()


@ray.remote(num_gpus=1, max_calls=1)
def classification(name):
    # loads ZSC from huggingface
    classifier = pipeline('zero-shot-classification', device=device, model=bart)

    # seq = get_sequence('assets/UserStoriesWithComponents_cleaned_filtered_no_title.csv', ['Type', 'Component_Names', 'TitleAndDescription'], 'TitleAndDescription')
    seq = get_sequence('final_assets/UserStoriesWithComponents_removed-grouped-8000.csv',
                       ['ID', 'Description', 'Type', 'Component_Names'], 'Description')
    seq = seq[:3]
    labels = get_labels('final_assets/removed-grouped-8000_comps.csv', ';')
    start = timer()
    results = classifier(seq, labels, multi_label=True)
    end = timer()
    print(end-start)
    print("Done")
    return results, seq


results,seq = ray.get(classification.remote(name))
# classification(name)

with open('final_assets/Output/' + name + '.txt', 'w', encoding='utf-8') as f:
    for story, result in zip(seq, results):
        f.write(f"Story: {story}\n")
        for label, score in zip(result['labels'], result['scores']):
            f.write(f"- {label}: {score:.2f}\n")

read_url = url + '.txt'
save_url = url + '.csv'
keyword = 'Story'
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
