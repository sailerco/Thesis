import csv

import pandas as pd
import yaml

user_stories = pd.read_csv('assets/UserStoriesWithComponents_cleaned_filtered_no_title.csv', delimiter=None, sep=None)
user_stories.columns = ['ID', 'Description', 'Type', 'Component_Names']


def count_comps():
    components = {}
    # Iterate over each row in the DataFrame to process the user stories and their components
    for index, row in user_stories.iterrows():
        skills = [skill.strip() for skill in row['Component_Names'].split(', ')]

        for skill in skills:
            components[skill] = components.get(skill, 0) + 1

    # Sort the list based on the number of occurrences (values)
    sorted_data_dict = dict(sorted(components.items(), key=lambda x: x[1], reverse=True))
    small_occ = {item for item, number in sorted_data_dict.items() if number == 1}
    return small_occ


def remove_unnecessary(stories, removable):
    for index, row in stories.iterrows():
        skills = [skill.strip() for skill in row['Component_Names'].split(', ')]
        updated_skills = [skill for skill in skills if skill not in removable]
        if len(updated_skills) != 0:
            stories.at[index, 'Component_Names'] = ', '.join(updated_skills)
        else:
            stories = stories.drop(index)
    return stories


def count(data):
    unique = set()
    for index, row in data.iterrows():
        skills = [skill.strip() for skill in row['Component_Names'].split(', ')]
        for skill in skills:
            unique.add(skill)
    return unique


def reduce_groups(remaining_data):
    with open('assets/components/reduced_comps.yml', 'r') as file:
        data = yaml.safe_load(file)
    for index, row in remaining_data.iterrows():
        skills = [skill.strip() for skill in row['Component_Names'].split(', ')]
        updated_skills = []
        for skill in skills:
            found = False
            for r, values in data.items():
                if skill in values:
                    updated_skills.append(r)
                    found = True
                    break
            if not found:
                updated_skills.append(skill)
        remaining_data.at[index, 'Component_Names'] = ', '.join(updated_skills)
    return remaining_data


def save_components(data, url):
    uniq = count(data)
    uniq = list(uniq)
    print(len(uniq))
    with open(f'assets/{url}_comps.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for value in uniq:
            writer.writerow([value])


url = "remain_reduce"
removable = count_comps()
user_stories = remove_unnecessary(user_stories, removable)
user_stories = reduce_groups(user_stories)
user_stories.to_csv(f'assets/UserStoriesWithComponents_{url}.csv', index=False)
save_components(user_stories, url)
