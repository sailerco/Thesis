import pandas as pd
import random

"""
    random skills were chosen, which were then fed in a specific prompt to a language model to get a user story
"""
data = pd.read_csv('../datasets/roles_small.csv')

def select_role_and_skills():
    row = random.choice(data.index)
    selected_role = data.loc[row, 'Job Role']
    selected_skills = data.loc[row, 'skill']
    # Convert the string of skills to a list
    selected_skills = selected_skills.split(', ')
    random_number = random.uniform(0.2, 0.6)
    sample_size = int(len(selected_skills) * random_number)
    random_skills = random.sample(selected_skills, sample_size)
    return selected_role, random_skills

for x in range(100):
    role, skills = select_role_and_skills()
    print("Randomly Selected Role:", role)
    print("Selected Skills:", skills)

