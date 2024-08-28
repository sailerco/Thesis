import pandas as pd

# Load the CSV into a DataFrame
df = pd.read_csv('PostFineTuning/bart_all_labels_6Eps.csv')

# Set the threshold
threshold = 0.7

# Iterate through the DataFrame and filter skills with scores above the threshold, skip the first row
for column in df.columns[1:]:
    print(f"\n{column}:")

    # Filter and sort the skills based on scores in descending order
    filtered_df = df[df[column] > threshold].sort_values(by=column, ascending=False)

    if not filtered_df.empty:
        print(len(filtered_df))
        result = ', '.join([f"{skill} ({score})" for skill, score in zip(filtered_df['Skills'], filtered_df[column])])
        print(result)
    else:
        print("None")