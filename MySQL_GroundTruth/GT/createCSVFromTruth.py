import csv

import pandas as pd
url = 'truth.csv'

user_stories = pd.read_csv('../assets/UserStoriesWithComponents_cleaned_filtered_no_title.csv', delimiter=None, sep=None)
user_stories.columns = ['ID', 'Description', 'Type', 'Component_Names']

stories = {}
# Iterate over each row in the DataFrame to process the user stories and their components
for index, row in user_stories.iterrows():
    story = row['Description']
    skills = [skill.strip() for skill in row['Component_Names'].split(',')]
    stories[story] = {skill: 1.0 for skill in skills}

output_data = {}
for skill, components in stories.items():
    for component, weight in components.items():
        output_data.setdefault(component, {})[skill] = weight

# Schreiben der Daten in eine CSV-Datei
with open('truth.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    cleaned_headers = ['Skills']+[header.strip().strip('"') for header in list(stories.keys())]
    writer.writerow(cleaned_headers)
    for component, values in output_data.items():
        row = [component] + [values.get(skill, '') for skill in stories.keys()]
        writer.writerow(row)

# Read the CSV file into a DataFrame and sort it
df = pd.read_csv(url, encoding='ISO-8859-1')
df_sorted = df.sort_values(by='Skills')
df_sorted.to_csv(url, index=False)

