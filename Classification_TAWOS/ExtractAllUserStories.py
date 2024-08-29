import mysql.connector
import csv

import pandas as pd

"""
    This script extracts user stories from the TAWOS database, processes them, 
    and saves the results to a CSV file. The user stories are filtered based 
    on specific criteria, and components from a provided CSV file are used to 
    query the database.
"""

fields = ['ID', 'Description', 'Type', 'Component_Names']


def read():
    """
    Reads the CSV file containing manually reduced component names and returns them as a list.

    Returns:
        list: A list of component names extracted from the CSV file.
    """
    csv_values = []
    with open('assets/components/cleaned.csv', 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csv_values.extend(row)
    return csv_values


def save(column_names, data):
    """
    Saves the extracted user stories to a CSV file.

    Args:
        column_names (list): The header for the CSV file.
        data (list): The list of rows containing user stories to be saved.
    """
    with open('assets/UserStoriesWithComponents_cleaned_filtered_no_title.csv', 'w', newline='',
              encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)
        for row in data:
            csvwriter.writerow(row)


def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="mysql"
    )
    return connection.cursor()


def extract_user_stories(csv_values, column_names):
    """
    Extracts user stories from the TAWOS database using the filtered component names
    provided in the CSV file. The user stories are filtered based on the presence
    of certain keywords and conditions.

    Args:
        csv_values (list): A list of component names used for filtering the query.
        column_names (list): The column names for the output CSV file.
    """

    cursor = connect_to_database()

    # SQL query template for extracting user stories based on
    # components and specific conditions as well as user story specific pattern
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

    # Construct the placeholders for the SQL query based on CSV values
    placeholders = ', '.join([f"'{x}'" for x in csv_values])
    # Format the SQL query by replacing placeholders with actual component names
    final_query = new_query.format(placeholders)

    # Execute the query and fetch the results
    cursor.execute(final_query)
    data = cursor.fetchall()

    # Save the extracted user stories to a CSV file
    save(column_names, data)


extract_user_stories(read(), fields)
