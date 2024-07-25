import mysql.connector
import csv

# extracts components from Tawos dataset
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mysql"
)

cursor = connection.cursor()

query = "SELECT DISTINCT Name FROM paper.component"

cursor.execute(query)

unique_values = cursor.fetchall()

with open('component.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(unique_values)