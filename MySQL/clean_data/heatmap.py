import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create(title, name, url):
    # Load data from CSV
    data = pd.read_csv(url + "output_" + name + '.csv', header=0, index_col=0,
                       encoding='ISO-8859-1')  # Update with your file path
    print(data)
    # Calculate correlation matrix
    # corr = data.corr()

    # Create correlation heatmap
    plt.figure(figsize=(40, 40))
    heatmap = sns.heatmap(data, cmap='Blues', annot=False)
    plt.title(title)
    plt.savefig(url + 'heatmap_' + name + '.png')

create('Full - Sileod', 'sileod', 'unfilteredCSV/')

"""create('3 Komponenten - DeBERTa', '3_comps', '3_comps/')
create('3 Komponenten - DeBERTa - large', '3_comps_large', '3_comps/')
create('3 Komponenten - Bart', '3_comps_bart', '3_comps/')

create('Filter 60% - DeBERTa', 'filtered', 'largerThan60%/')
create('Filter 60% - DeBERTa - large', 'filtered_large', 'largerThan60%/')
create('Filter 60% - Bart', 'filtered_bart', 'largerThan60%/')

create('Full - DeBERTa', '', 'unfilteredCSV/')
create('Full - DeBERTa - large', 'large', 'unfilteredCSV/')
create('Full - Bart', 'bart', 'unfilteredCSV/')

create('Full - Reversed', 'reverse', 'unfilteredCSV/')
create('Filter 60% - Reversed', 'reverse', 'largerThan60%/')
create('3 Komponenten - Reversed', 'reverse', '3_comps/')"""
