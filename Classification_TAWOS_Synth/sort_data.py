import pandas as pd

"""
    if the ground truth file isn't sorted then please use this function
"""

df = pd.read_csv("truth.csv", encoding='ISO-8859-1')
df_sorted = df.sort_values(by='Skills')
df_sorted.to_csv("truth.csv", index=False)
