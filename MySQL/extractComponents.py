import mysql.connector
import csv
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mysql"
)

cursor = connection.cursor()

# Replace 'your_table' with the actual table name and 'your_column' with the column name
query = "SELECT DISTINCT Name FROM paper.component"

cursor.execute(query)

unique_values = cursor.fetchall()

with open('DataFromDB/component.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(unique_values)