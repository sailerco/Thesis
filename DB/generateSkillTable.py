import pandas as pd
import psycopg2 as psg
import csv


"""
    This script populates the skills table in a PostgreSQL database 
    with unique skills extracted from a CSV file (roles_small.csv).
"""
conn = psg.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

df = pd.read_csv('/DB/datasets/roles_small.csv')  # Update with your CSV file path
df.columns = ['role', 'description', 'skills']
unique_skills = set()
for skills in df['skills'].dropna():
    for skill in skills.split(','):
        if skill.strip() not in unique_skills:
            unique_skills.add(skill.strip())
print(unique_skills)
for skill in unique_skills:
    cur.execute("INSERT INTO skills(skill) VALUES (%s)", (skill,))
conn.commit()
conn.close()