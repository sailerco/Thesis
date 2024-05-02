import psycopg2 as psg
import csv
import random

used_names = set()
prof = ['BEGINNER', 'INTERMEDIATE', 'PROFESSIONAL']
roles_employees_count = {}

def main():
    # Function to read random names from a CSV file without duplicates
    def get_random_name():
        with open('D:/Thesis/DB/datasets/randomNames.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            names = [row for row in reader if row[0] not in used_names]
        if not names:
            raise ValueError("All names have been used")
        random_row = random.choice(names)
        random_fname = random_row[0]
        random_lname = random_row[1]
        return random_fname, random_lname

    random_name = get_random_name()
    used_names.add(random_name)
    print(random_name)

    conn = psg.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # 1. Insert employee with random name and random role
    cur.execute("SELECT role_id, role FROM roles")
    roles = [record for record in cur.fetchall()]
    roles_without_employee = [role for role in roles if roles_employees_count.get(role[1], 0) == 0]

    if not roles_without_employee:
        role = random.choice(roles)
    else:
        role = random.choice(roles_without_employee)

    roles_employees_count[role[1]] = roles_employees_count.get(role[1], 0) + 1
    print(roles_employees_count)
    cur.execute("INSERT INTO employees (first_name, last_name, role_id) VALUES (%s, %s, %s)",
                (random_name[0], random_name[1], int(role[0])))
    conn.commit()

    # 2. retrieve the skills of the role
    def get_skills_of_role(role):
        with open('D:/Thesis/DB/datasets/Roles_small.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if row[0] == role:
                    return row[2]

    skills = get_skills_of_role(role[1]).split(",")
    skills = [skill.strip() for skill in skills]
    print(skills)

    # 3. get a random amount of skills from the skill set
    random_number = random.uniform(0.6, 1)
    sample_size = int(len(skills) * random_number)
    random_skills = random.sample(skills, sample_size)
    print(random_skills)
    skill_set = set()
    for skill_name in random_skills:
        query = "SELECT skill_id FROM skills WHERE skill = %s"
        cur.execute(query, (skill_name,))
        skill_set.add(cur.fetchone()[0])

    # 4. generate entry in employee_skills
    cur.execute("SELECT employee_id FROM employees where first_name = %s AND last_name = %s", (random_name[0], random_name[1]))
    employee_id = cur.fetchone()[0]
    for skill_id in skill_set:
        cur.execute("INSERT INTO employee_skills (employee_id, skill_id, proficiency_lvl) VALUES (%s, %s, %s)",
                    (int(employee_id), int(skill_id), random.choice(prof)))
    conn.commit()


for i in range(50):
    main()
