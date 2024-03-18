from be_great import GReaT
from sklearn.datasets import fetch_california_housing
import csv
import pandas as pd

data = pd.read_csv('DB/output/joined_data.csv')
model = GReaT(llm='distilgpt2', batch_size=32, epochs=25)
model.fit(data)
synthetic_data = model.sample(n_samples=100)