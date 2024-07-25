import mysql.connector
import csv

import pandas as pd

"""
    used to extract user stories from TAWOS database
"""

fields = ['ID', 'Description', 'Type', 'Component_Names']


def read():
    csv_values = []
    with open('assets/components/cleaned.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_values.extend(row)
    return csv_values


def save(column_names, data):
    with open('assets/UserStoriesWithComponents_cleaned_filtered_no_title_2.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        for row in data:
            csvwriter.writerow(row)


def extract_user_stories(csv_values, column_names):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="mysql"
    )
    cursor = connection.cursor()
    new_query = """
    SELECT i.ID, i.Description, i.Type, GROUP_CONCAT(c.Name) AS Component_Names
    FROM paper.issue AS i
    INNER JOIN paper.issue_component ic ON i.ID = ic.Issue_ID
    INNER JOIN paper.component c ON ic.Component_ID = c.ID
    WHERE c.Name IN ({}) 
      AND Title NOT LIKE '%http%'
      AND i.Description NOT LIKE '%http%'
      AND (i.Description LIKE '%As a%' OR i.Description LIKE 'we')
      AND (i.Description LIKE '%I want%'
               OR i.Description LIKE '%I would%'
               OR i.Description LIKE "%I\'%"
               OR i.Description LIKE '%I need%'
          )
    GROUP BY i.ID
    """

    # Constructing the placeholders for the CSV values#
    placeholders = ', '.join([f"'{x}'" for x in csv_values])
    # Adding the placeholders to the query and executing the new SQL query with the CSV values
    final_query = new_query.format(placeholders)

    cursor.execute(final_query)
    data = cursor.fetchall()
    save(column_names, data)


def merge(column_names):
    # compares two sets (Used to see if all skills were used in the user stories)
    data = pd.read_csv('assets/UserStoriesWithComponents_cleaned_filtered.csv')
    data.columns = column_names
    df = pd.DataFrame(data)
    df['TitleAndDescription'] = df['Title'] + " | Description: " + df['Description']
    df = df.drop(columns=['ID', 'Title', 'Description'])
    df.to_csv('assets/Merged_UserStoriesWithComponents_cleaned_filtered.csv', header=True, index=False)


extract_user_stories(read(), fields)
#merge(fields)
