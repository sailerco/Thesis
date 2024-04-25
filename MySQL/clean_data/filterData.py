with open('D:/Thesis/MySQL/ClassifierOutput/reversedComponentAndSkills_bart.txt', 'r') as f:
    data = f.readlines()


def is_not_float(string):
    try:
        float(string)
        return False
    except ValueError:
        return True


filtered_data = [row for row in data if (is_not_float(row.split(':')[-1]) or float(row.split(':')[-1]) >= 0.6)]
"""count = 0
filtered_data = []
for row in data:
    comp = row.split(':')[-1]
    if is_not_float(comp):
        count = 0
        filtered_data.append(row)
    elif count < 3:
        count = count + 1
        filtered_data.append(row)
"""
# Save the filtered data to a new text file
with open('largerThan60%/filtered_reversed.txt', 'w') as file:
    file.writelines(filtered_data)
