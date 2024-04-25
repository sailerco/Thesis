import csv
import pandas as pd

url = 'unfilteredCSV/sileod.csv'
# Einlesen der Textdatei
with open('../ClassifierOutput/skills_classification_sileod.txt', 'r') as file:
    lines = file.readlines()

# Erstellen eines leeren Dictionaries, um die Daten zu speichern
data = {}

skill = None
for line in lines:
    if line.strip():  # Überprüfen, ob die Zeile nicht leer ist
        key, value = line.replace("\n", "").rsplit(': ', 1)
        #key, value = line.replace("\n", "").split(': ', 1)
        if key.startswith('Skill'):
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
