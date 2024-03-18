import psycopg2 as psg
import csv

conn = psg.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Write the SQL query to join the tables based on parameters
query = """
SELECT first_name, last_name, role, skill, proficiency_lvl
FROM employee_skills as es 
JOIN employees as e ON es.employee_id = e.employee_id
JOIN skills ON es.skill_id = skills.skill_id
JOIN roles ON e.role_id = roles.role_id
"""

# Execute the query
cur.execute(query)

# Fetch the joined data
joined_data = cur.fetchall()

# Specify the path and filename of the CSV file
csv_filename = 'DB/output/joined_data.csv'
headerList = ['first_name', 'last_name', 'role', 'skill', 'proficiency_lvl']
# Write the joined data to the CSV file
with open(csv_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headerList)
    writer.writerows(joined_data)