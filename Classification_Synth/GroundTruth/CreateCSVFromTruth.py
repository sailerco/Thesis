import csv
import pandas as pd

"""
    Creating the Ground Truth from the user stories csv file
"""

url = 'truth.csv'

user_stories = pd.read_csv('../userStories.csv', delimiter=';', usecols=[0, 1])
user_stories.columns = ['user_stories', 'skills']

stories = {}
for index, row in user_stories.iterrows():
    story = row['user_stories']
    skills = row['skills'].replace("'", "").split(', ')
    stories[story] = {}
    for skill in skills:
        print(skill)
        if skill.startswith(" "):
            skill = skill.replace(" ", "", 1)
        stories[story][skill] = 1.0

output_data = {}
for skill, components in stories.items():
    for component, weight in components.items():
        if component not in output_data:
            output_data[component] = {}
        output_data[component][skill] = weight

# write data in CSV file
with open('truth.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    cleaned_headers = [header.strip().strip('"') for header in list(stories.keys())]
    cleaned_headers.insert(0, 'Skills')
    writer.writerow(cleaned_headers)
    for component, values in output_data.items():
        row = [component] + [values.get(skill, '') for skill in stories.keys()]
        writer.writerow(row)

# Sort it into the correct format
df = pd.read_csv(url, encoding='ISO-8859-1')
df_sorted = df.sort_values(by='Skills')
df_sorted.to_csv(url, index=False)
