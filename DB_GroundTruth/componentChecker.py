import pandas as pd

# compares two sets (Used to see if all skills were used in the user stories)
data = pd.read_csv('../DB/datasets/skills.csv', header=None)
user_stories = pd.read_csv('userStories.csv', delimiter=';', usecols=[0,1])
user_stories.columns = ['user_stories', 'skills']
unique_skills = set()
for skills in user_stories['skills'].dropna():
    skills = skills.replace("[", "").replace("]", "").replace("'", "")
    for skill in skills.split(','):
        if skill.strip() not in unique_skills:
            unique_skills.add(skill.strip())
data_set = set(data[0])
print(data_set - unique_skills)
