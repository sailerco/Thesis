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

HEADER = ["ID", "First Name", "Last Name", "Number of skills that overlap", "Skills that overlap"]
DEBERTA_PATH = "FineTuning/FinalRuns_PreTrained/deberta_08_10_2e-05_3232_0.1_0.06"
BART_PATH = "FineTuning/FinalRuns_PreTrained/bart_08_10_1e-05_3232_0.1_0.06"
CSV_PATH = "DB/datasets/skills.csv"

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def load_skills_data():
    df = pd.read_csv(CSV_PATH, header=None, encoding='ISO-8859-1')
    return df[0].tolist()


def choose_model():
    title = 'Welcome to the Skill Management Pipeline. Choose which Model should be used:'
    options = ['Bart Model', 'DeBERTa Model']
    option, index = pick(options, title)
    return BART_PATH if index == 0 else DEBERTA_PATH


def do_classification(premise, hypothesis, model):
    classifier = pipeline('zero-shot-classification', device=device, model=model)
    results = classifier(premise, hypothesis, multi_label=True)
    return {label: score for label, score in zip(results['labels'], results['scores']) if score > 0.7}


def connect_to_db():
    conn = psg.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )
    return conn, conn.cursor()


def generate_sql_query(skill_list):
    provided_skills_query = "WITH provided_skills AS (\n" + "\nUNION ALL\n".join(
        [f"SELECT '{skill}' AS skill" for skill in skill_list]
    ) + "\n)"

    return f"""
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


def fetch_employee_data(conn, cur, skills_list):
    sql_query = generate_sql_query(skills_list)
    cur.execute(sql_query)
    conn.commit()
    data = cur.fetchall()
    table = []
    for row in data:
        table.append(row)
    print(tabulate(table, headers=HEADER))
    conn.close()


labels = load_skills_data()
model_name = choose_model()
input_story = input("Please enter a user story: ")
skills_above_threshold = do_classification(input_story, labels, model_name)
skills = list(skills_above_threshold.keys())
print(skills_above_threshold)
conn, cur = connect_to_db()
fetch_employee_data(conn, cur, skills)
