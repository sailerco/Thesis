import csv

import pandas as pd

#url = "D:/Thesis/MySQL_GroundTruth/ClassifierOutput/deberta_remain_reduce_8000"
url = "D:/Thesis/MySQL_GroundTruth/final_assets/Output/deberta_removed"
read_url = url + '.txt'
save_url = url + '.csv'
keyword = 'Story'
with open(read_url, 'r', encoding='utf-8') as file:
    lines = file.readlines()
print(len(lines)/208)

# dictonary, data is going to be saved to
data = {}
skill = None
for line in lines:
    if line.strip():
        if line.startswith(keyword):
            key, value = line.replace("\n", "").split(': ', 1)
            skill = value
            print(skill)
            data[skill] = {}
        else:
            key, value = line.replace("\n", "").rsplit(': ', 1)
            component, weight = key.replace("- ", "", 1), float(value)
            data[skill][component] = weight
    else:
        print("yes")
print(len(data))

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