import CsvConverter as conv


def is_not_float(string):
    try:
        float(string)
        return False
    except ValueError:
        return True


def filter_60(data):
    filtered_data = [row for row in data if (is_not_float(row.split(':')[-1]) or float(row.split(':')[-1]) >= 0.6)]
    return filtered_data


def filter_top_three(data):
    count = 0
    filtered_data = []
    for row in data:
        comp = row.split(':')[-1]
        if is_not_float(comp):
            count = 0
            filtered_data.append(row)
        elif count < 3:
            count = count + 1
            filtered_data.append(row)
    return filtered_data


url = '../ClassifierOutput/skills_classification_'
names = ['bart', 'deberta_base', 'deberta_large']

for name in names:
    with open(url + name + '.txt', 'r') as f:
        data = f.readlines()
    percent = filter_60(data)
    top = filter_top_three(data)
    with open(f'largerThan60%/filtered_{name}.txt', 'w') as file:
        file.writelines(percent)
    with open(f'3_comps/filtered_{name}.txt', 'w') as f:
        f.writelines(top)
    csv = conv.CsvConverter('D:/Thesis/MySQL/clean_data/largerThan60%/filtered_' + name + '.txt',
                            'D:/Thesis/MySQL/clean_data/largerThan60%/filtered_' + name + '.csv', 'Skill')
    csv.convert()
    csv = conv.CsvConverter('D:/Thesis/MySQL/clean_data/3_comps/filtered_' + name + '.txt',
                            'D:/Thesis/MySQL/clean_data/3_comps/filtered_' + name + '.csv', 'Skill')
    csv.convert()
