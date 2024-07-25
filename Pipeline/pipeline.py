print("Loading data...")

import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

import pandas as pd
import psycopg2 as psg
import torch
from pick import pick
from tabulate import tabulate
from transformers import pipeline

"""
   Pipeline to get the most suitable employees for the specific user story 
"""

header = ["ID", "First Name", "Last Name", "Number of skills that overlap", "Skills that overlap"]

deberta_path = "FineTuning/FinalRuns_PreTrained/deberta_6_2e-05_3232_0.1_0.06"
bart_path = "FineTuning/FinalRuns_PreTrained/6_1e-05_3232_0.1_0.06"
df = pd.read_csv('DB/datasets/skills.csv', header=None, encoding='ISO-8859-1')
labels = df[0].tolist()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

title = 'Skill Management Pipeline Choose which Model should be used'
options = ['Bart Model', 'DeBERTa Model']
option, index = pick(options, title)
input_story = input("Please enter a user story: ")

model_name = bart_path if index == 0 else deberta_path

classifier = pipeline('zero-shot-classification', device=device, model=model_name)
results = classifier(input_story, labels, multi_label=True)

skills_above_threshold = {label: score for label, score in zip(results['labels'], results['scores']) if score > 0.7}
skills = list(skills_above_threshold.keys())
print(skills_above_threshold)
conn = psg.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

provided_skills_query = "WITH provided_skills AS (\n" + "\nUNION ALL\n".join(
    [f"SELECT '{skill}' AS skill" for skill in skills]
) + "\n)"

sql_query = f"""
{provided_skills_query}

SELECT e.employee_id, e.first_name, e.last_name, COUNT(s.skill_id) AS overlapping_skills,
       STRING_AGG(s.skill || ' (' || es.proficiency_lvl || ')', ', ' ORDER BY s.skill) AS overlapping_skill_names
FROM employees e
         JOIN employee_skills es ON e.employee_id = es.employee_id
         JOIN skills s ON es.skill_id = s.skill_id
         JOIN provided_skills ps ON s.skill = ps.skill
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY overlapping_skills DESC, e.employee_id;
"""

cur.execute(sql_query)
conn.commit()
data = cur.fetchall()
table = []
for row in data:
    table.append(row)
print(tabulate(table, headers=header))

conn.close()
