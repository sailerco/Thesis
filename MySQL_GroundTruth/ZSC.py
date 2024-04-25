import csv

import pandas as pd
from transformers import pipeline

"""
ZSC + NLI to match user stories to components 
"""

url_name = "bart"
def get_sequence(url, columns, column):
    sequence = pd.read_csv(url)
    sequence.columns = columns
    return sequence[column].tolist()


def get_labels(url, delimiter):
    df = pd.read_csv(url, header=None, encoding='ISO-8859-1', delimiter=delimiter)
    return df[0].tolist()


def classification(name):
    # loads ZSC from huggingface
    bart = "facebook/bart-large-mnli"
    deberta_base = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    deberta_large = "MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli"
    sileod = 'sileod/deberta-v3-base-tasksource-nli'
    classifier = pipeline('zero-shot-classification', model=bart)

    seq = get_sequence('assets/Merged_UserStoriesWithComponents_cleaned_filtered.csv',
                       ['Type', 'Component_Names', 'TitleAndDescription'], 'TitleAndDescription')
    labels = get_labels('assets/cleaned.csv', ';')

    # do the classification
    results = classifier(seq, labels, multi_label=True)

    with open('ClassifierOutput/' + name + '.txt', 'w') as f:
        for story, result in zip(seq, results):
            f.write(f"Story: {story}\n")
            for label, score in zip(result['labels'], result['scores']):
                f.write(f"- {label}: {score:.2f}\n")
    print("Done")


classification(url_name)


def convert_to_csv(name):
    url = 'ClassifierOutput/' + name + '.csv'
    with open('ClassifierOutput/' + name + '.txt', 'r') as file:
        lines = file.readlines()

    # dictonary, data is going to be saved to
    data = {}
    skill = None
    for line in lines:
        if line.strip():
            key, value = line.replace("\n", "").rsplit(': ', 1)
            print(key, value)
            if key.startswith('Story'):
                skill = value
                data[skill] = {}
            else:
                component, weight = key.replace("- ", "", 1), float(value)
                data[skill][component] = weight

    # Umformatierung der Daten in ein geeignetes Format für den CSV-Export
    output_data = {}
    for skill, components in data.items():
        for component, weight in components.items():
            if component not in output_data:
                output_data[component] = {}
            output_data[component][skill] = weight

    # Schreiben der Daten in eine CSV-Datei
    with open(url, 'w', newline='') as file:
        writer = csv.writer(file)
        # Schreiben der Spaltenüberschriften
        cleaned_headers = [header.strip().strip('"') for header in list(data.keys())]
        cleaned_headers.insert(0, 'Skills')
        writer.writerow(cleaned_headers)
        for component, values in output_data.items():
            row = [component] + [values.get(skill, '') for skill in data.keys()]
            writer.writerow(row)

    # Read the CSV file into a DataFrame and sort it
    df = pd.read_csv(url, encoding='ISO-8859-1')
    df_sorted = df.sort_values(by='Skills')
    df_sorted.to_csv(url, index=False)


convert_to_csv(url_name)
