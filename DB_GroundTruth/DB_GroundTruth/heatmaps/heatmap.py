import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create(title, name, url):
    # Load data from CSV
    data = pd.read_csv(url + "" + name + '.csv', header=0, index_col=0,
                       encoding='ISO-8859-1')  # Update with your file path
    print(data)
    # Calculate correlation matrix
    # corr = data.corr()

    # Create correlation heatmap
    plt.figure(figsize=(40, 40))
    heatmap = sns.heatmap(data, cmap='Blues', annot=False)
    plt.title(title)
    plt.savefig('heatmap_' + name + '.png')

create('Bart', 'bart', '../ClassifierOutput/')
create('deberta', 'deberta_base', '../ClassifierOutput/')
create('Ground Truth', 'truth', '../GT/')
