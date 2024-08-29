import csv
import re
import pandas as pd
import yaml

"""
    preprocessing of the TAWOS dataset by either grouping, reducing or both
"""

user_stories = pd.read_csv('assets/UserStoriesWithComponents_cleaned_filtered_no_title.csv', delimiter=None, sep=None)
user_stories.columns = ['ID', 'Description', 'Type', 'Component_Names']

PATH_NAME = "8000"

group_similar_components_flag = True
reduce_infrequent_components_flag = False

if group_similar_components_flag and reduce_infrequent_components_flag:
    PATH_NAME = f"removed-grouped-{PATH_NAME}"
elif group_similar_components_flag:
    PATH_NAME = f"grouped-{PATH_NAME}"
elif reduce_infrequent_components_flag:
    PATH_NAME = f"removed-{PATH_NAME}"


def count_component_occurrences():
    """
    Counts the occurrences of each component in the 'Component_Names' column of the user stories DataFrame.

    Returns:
        small_occ (set): A set of components that appear only once in the user stories.
    """
    components = {}

    # Iterate over each row in the DataFrame to process the user stories and their components
    for index, row in user_stories.iterrows():
        skills = [skill.strip() for skill in re.split(r',(?!\s)', row['Component_Names'])]
        for skill in skills:
            components[skill] = components.get(skill, 0) + 1

    # Sort the list based on the number of occurrences (values)
    sorted_data_dict = dict(sorted(components.items(), key=lambda x: x[1], reverse=True))
    print(sorted_data_dict)
    small_occ = {item for item, number in sorted_data_dict.items() if number == 1}
    return small_occ


def remove_infrequent_components(stories, removable):
    """
    Removes components from the user stories that are considered unnecessary (appear only once).

    Args:
        stories (pd.DataFrame): The DataFrame containing user stories.
        removable (set): A set of components to be removed from the user stories.

    Returns:
        pd.DataFrame: The updated DataFrame with unnecessary components removed.
    """
    for index, row in stories.iterrows():
        skills = [skill.strip() for skill in re.split(r',(?!\s)', row['Component_Names'])]
        # skills = [skill.strip() for skill in row['Component_Names'].split(', ')]
        updated_skills = [skill for skill in skills if skill not in removable]
        if len(updated_skills) != 0:
            stories.at[index, 'Component_Names'] = ','.join(updated_skills)
        else:
            stories = stories.drop(index)
    return stories


def filter_long_user_stories(stories):
    """
    Removes user stories with descriptions longer than 8192 characters from the DataFrame.

    Args:
        stories (pd.DataFrame): The DataFrame containing user stories.

    Returns:
        pd.DataFrame: The updated DataFrame with long descriptions removed.
    """
    for index, row in stories.iterrows():
        us = row['Description']
        if len(us) > 8192:
            stories = stories.drop(index)
    return stories


def extract_unique_components(data):
    """
    Extracts the unique components in the 'Component_Names' column of the user stories DataFrame.

    Args:
        data (pd.DataFrame): The DataFrame containing user stories.

    Returns:
        unique (set): A set of unique components found in the user stories.
    """
    unique = set()
    for index, row in data.iterrows():
        skills = [skill.strip() for skill in re.split(r',(?!\s)', row['Component_Names'])]
        # skills = [skill.strip() for skill in row['Component_Names'].split(', ')]
        for skill in skills:
            unique.add(skill)
    return unique


def group_similar_components(remaining_data):
    """
    Reduces the components in the user stories based on groupings defined in a YAML file.
    Components that belong to the same group are replaced by their representative group name.

    Args:
        remaining_data (pd.DataFrame): The DataFrame containing user stories.

    Returns:
        pd.DataFrame: The updated DataFrame with grouped components.
    """
    with open('assets/components/grouped_comps.yml', 'r') as file:
        data = yaml.safe_load(file)
    for index, row in remaining_data.iterrows():
        skills = [skill.strip() for skill in re.split(r',(?!\s)', row['Component_Names'])]
        # skills = [skill.strip() for skill in row['Component_Names'].split(', ')]
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
        remaining_data.at[index, 'Component_Names'] = ','.join(updated_skills)
    return remaining_data


def save_components(data):
    """
    Saves the unique components from the user stories DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): The DataFrame containing user stories.
    """
    unique = list(extract_unique_components(data))
    unique.sort()
    print(len(unique))
    with open(f'final_assets/{PATH_NAME}_comps.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for value in unique:
            writer.writerow([value])


user_stories = filter_long_user_stories(user_stories)

if reduce_infrequent_components_flag:
    removable = count_component_occurrences()
    user_stories = remove_infrequent_components(user_stories, removable)

if group_similar_components_flag:
    user_stories = group_similar_components(user_stories)

user_stories = user_stories.drop_duplicates(subset=["Description"])
# save user stories and components
user_stories.to_csv(f'final_assets/UserStoriesWithComponents_{PATH_NAME}.csv', index=False)

# just save components
save_components(user_stories)
