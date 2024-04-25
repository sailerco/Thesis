import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the CSV files
file1 = '../clean_data/unfilteredCSV/output.csv'
file2 = '../clean_data/unfilteredCSV/output_bart.csv'
file3 = '../clean_data/unfilteredCSV/output_large.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)

# Step 2: Feature Extraction
skills = list(df1.columns)  # Assuming the column headers represent the skills

# Step 3: Similarity Measurement
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df1.values.astype(str))  # Convert to string to ensure numeric values are treated as text
similarity_matrix = cosine_similarity(X)

# Step 4: Clustering
num_clusters = 3  # Choose an appropriate number of clusters
kmeans = KMeans(n_clusters=num_clusters, random_state=0)
clusters = kmeans.fit_predict(similarity_matrix)

print(clusters)
# Step 5: Building a Matching Mechanism
# You can build a lookup table to associate each component with its cluster
#component_cluster_mapping = dict(zip(df1.index, clusters))
