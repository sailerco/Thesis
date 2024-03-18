import psycopg2
import pandas as pd

# Load roles and descriptions from CSV file into a DataFrame
roles_df = pd.read_csv('D:\Thesis\DB\Rolesandtheirwork.csv')  # Update with your CSV file path
roles_df.columns = ['role', 'description']  # Assuming columns are 'role' and 'description'

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Retrieve roles from the PostgreSQL table
cur.execute("SELECT role FROM roles")
db_roles = [record[0] for record in cur.fetchall()]
# Map descriptions to roles and update PostgreSQL table
for index, row in roles_df.iterrows():
    if row['role'] in db_roles:
        cur.execute("UPDATE roles SET description = %s WHERE role = %s", (row['description'], row['role']))

conn.commit()
conn.close()