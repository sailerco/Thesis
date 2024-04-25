import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def transpose_reverse(name):
    # transpose bart csv
    df_reversed = pd.read_csv(f'../{name}.csv')
    df_reversed = df_reversed.T
    df_reversed.to_csv(f'{name}_transposed.csv', header=False)
    df_reversed = pd.read_csv(f'{name}_transposed.csv', header=0)
    df_reversed = df_reversed.sort_values(by='Skills')
    df_reversed.to_csv(f'{name}_transposed.csv', index=False)


def sort_columns(name):
    normal = pd.read_csv(f'../{name}.csv')
    # Store the row headers in a separate series
    row_headers = normal.iloc[:, 0]
    # Sort the columns alphabetically, excluding the first column (index 0, which contains row headers)
    df_sorted = normal.iloc[:, 1:].sort_index(axis=1)
    # Combine the sorted columns with the row headers
    df_sorted = pd.concat([row_headers, df_sorted], axis=1)
    df_sorted.to_csv(f'{name}_sorted.csv', index=False)


# transpose_reverse('output_reverse')
# sort_columns('output_bart')

def compare(reversed, normal):
    data1 = pd.read_csv(reversed)
    data2 = pd.read_csv(normal)
    similarity_matrix = cosine_similarity(data1.iloc[:, 1:], data2.iloc[:, 1:])
    # Mittlere Ähnlichkeit berechnen
    mean_similarity = similarity_matrix.mean()

    # Ausgabe des Ergebnisses
    if mean_similarity > 0.5:
        print("Die Felder stimmen gut überein.")
    else:
        print("Die Felder stimmen nicht besonders gut überein.")

    print("Durchschnittliche Ähnlichkeit:", mean_similarity)


compare('output_reverse_transposed.csv', 'output_bart_sorted.csv')
