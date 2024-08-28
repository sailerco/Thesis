import pandas as pd

"""
    select random user stories
"""


def get_sequence(url, columns, column):
    max_length = 200
    sequence = pd.read_csv(url, encoding='ISO-8859-1', delimiter=None, sep=None)
    sequence[column] = sequence[column].astype(str).str.replace('"', '')
    filtered_sequence = sequence[
        (sequence[column].apply(lambda x: x.strip().startswith("As a"))) & (sequence[column].str.len() <= max_length)]

    print((sequence[column].str.len() <= max_length))
    filtered_sequence = filtered_sequence.sample(25)
    filtered_sequence[column].to_csv("assets/jira2.csv")
    return sequence[column].tolist()


user_stories = get_sequence("../Classification_TAWOS/final_assets/UserStoriesWithComponents_removed-grouped-8000.csv",
                            ['ID', 'Description', 'Type', 'Component_Names'], 'Description')
