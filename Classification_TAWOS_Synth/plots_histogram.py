import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.metrics

"""
    Generating the histogram and distribution of predictions
"""

# CSV-Dateien laden
df_pre_ft = pd.read_csv('PreFineTuning/bart_all_labels.csv', index_col=0)
df_post_ft = pd.read_csv('PreFineTuning/deberta_all_labels.csv', index_col=0)

# Daten für Histogramme und Dichte-Plots vorbereiten
pre_ft_values = df_pre_ft.values.flatten()
post_ft_values = df_post_ft.values.flatten()

before_label = 'Before Fine-Tuning BART'
after_label = 'Before Fine-Tuning DeBERTa'
# Histogramme
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.hist(pre_ft_values, bins=50, alpha=0.7, label=before_label)
plt.hist(post_ft_values, bins=50, alpha=0.7, label= after_label)
plt.title('Histogram of Predictions')
plt.xlabel('Prediction Values')
plt.ylabel('Frequency')
#plt.xlim(0.2, 1.0)
#plt.ylim(0, 100)
#plt.ylim(0, 2600)  # Set y-axis limit
plt.legend()


# Dichte-Plots
plt.subplot(1, 2, 2)
sns.kdeplot(pre_ft_values, fill=True, label=before_label)
sns.kdeplot(post_ft_values, fill=True, label=after_label)
plt.title('Density Plot of Predictions')
plt.xlabel('Prediction Values')
plt.ylabel('Density')
#plt.ylim(0, 3)
#plt.xlim(0.2, 1.0)
plt.legend()

plt.tight_layout()
plt.show()

