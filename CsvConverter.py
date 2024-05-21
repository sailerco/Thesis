import csv

import pandas as pd


class CsvConverter:
    def __init__(self, read_url, save_url, keyword):
        self.read_url = read_url
        self.save_url = save_url
        self.keyword = keyword #should be string

    def convert(self):
        with open(self.read_url, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # dictonary, data is going to be saved to
        data = {}
        skill = None
        for line in lines:
            if line.strip():
                key, value = line.replace("\n", "").rsplit(': ', 1)
                #print(key, value)
                if key.startswith(self.keyword):
                    skill = value
                    data[skill] = {}
                else:
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
        with open(self.save_url, 'w', newline='') as file:
            writer = csv.writer(file)
            cleaned_headers = [header.strip().strip('"') for header in list(data.keys())]
            cleaned_headers.insert(0, 'Skills')
            writer.writerow(cleaned_headers)
            for component, values in output_data.items():
                row = [component] + [values.get(skill, '') for skill in data.keys()]
                writer.writerow(row)

        # Read the CSV file into a DataFrame and sort it
        df = pd.read_csv(self.save_url, encoding='ISO-8859-1')
        df_sorted = df.sort_values(by='Skills')
        df_sorted.to_csv(self.save_url, index=False)