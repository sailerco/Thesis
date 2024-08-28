import os
import pandas as pd
from transformers import pipeline
import CsvConverter as Conv
import torch

"""
    ZSC + NLI to match user stories to skills 
"""

PATH_NAME = 'deberta'
URL = "ClassifierOutput/" + PATH_NAME

BART = "facebook/bart-large-mnli"
DEBERTA = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"

#flag if a modified hypothesis template should be used
MODIFIED_HYPO_TEMP = False
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def get_user_stories():
    """extract the synthetic user stories"""
    df = pd.read_csv('userStories.csv', delimiter=';')
    df.columns = ['user_stories', 'skills']
    return df['user_stories'].tolist()


def get_skills():
    """loads skills from prepared csv files"""
    df = pd.read_csv('../DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
    return df[0].tolist()


def do_classification(hypothesis, labels):
    """load pipeline and do a zero-shot classification"""
    classifier = pipeline('zero-shot-classification', device=device, model=DEBERTA)
    # do the classification, either with or without a modified hypothesis template
    if MODIFIED_HYPO_TEMP:
        hypothesis_template = "To resolve this issue the skill {} is needed."
        return classifier(hypothesis, labels, multi_label=True, hypothesis_template=hypothesis_template)
    else:
        return classifier(hypothesis, labels, multi_label=True)


user_stories = get_user_stories()
skills = get_skills()
results = do_classification(user_stories, skills)


def save_in_txt():
    # save the resulting data in a text file
    with open(URL + ".txt", 'w') as f:
        for story, result in zip(user_stories, results):
            f.write(f"Story: {story}\n")
            for label, score in zip(result['labels'], result['scores']):
                f.write(f"- {label}: {score:.2f}\n")
    print("Done")


def save_in_csv():
    # convert the text file to a csv file
    file_dir = os.getcwd()
    csv = Conv.CsvConverter(os.path.join(file_dir, "ClassifierOutput", f'{PATH_NAME}.txt'),
                            os.path.join(file_dir, "ClassifierOutput", f'{PATH_NAME}.csv'), 'Story')
    csv.convert()


save_in_txt()
save_in_csv()
