import mysql.connector
import csv

"""
    so far no use but extracts users and how often they used their skills
"""
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="mysql"
)

cursor = connection.cursor()

query = """
SELECT UserComponents.ID, GROUP_CONCAT(ComponentWithWeight SEPARATOR ', ') as Components_with_Weight
FROM (
         SELECT u.ID, CONCAT(c.Name, ' (', COUNT(*) , ')') as ComponentWithWeight
         FROM paper.user u
                  INNER JOIN paper.issue i on u.ID = i.Assignee_ID
                  INNER JOIN paper.issue_component ic on i.ID = ic.Issue_ID
                  INNER JOIN paper.component c on ic.Component_ID = c.ID
         GROUP BY u.ID, c.Name
     ) AS UserComponents
GROUP BY UserComponents.ID;
"""

cursor.execute(query)

user_components = cursor.fetchall()

with open('UserComponents.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for user_id, components in user_components:
        writer.writerow([f"User {user_id} has components: {components}"])