import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

"""
    Generating the histogram and distribution of predictions
"""
PRE_BART_PATH = 'PreFineTuning/bart_all_labels.csv'
POST_BART_PATH = 'PostFineTuning/bart_all_labels_6Eps.csv'
PRE_DEBERTA_PATH = 'PreFineTuning/deberta_all_labels.csv'
POST_DEBERTA_PATH = 'PostFineTuning/deberta_all_labels_6Eps.csv'


def read_file(path_name):
    """Reads a CSV file and returns a DataFrame."""
    return pd.read_csv(path_name, index_col=0)


def get_meta_data(name, path, comparison_path):
    """Retrieves the pre and post fine-tuning data and prepares labels for the plots."""
    df_pre_ft = read_file(path)
    df_post_ft = read_file(comparison_path)
    if name is None:
        before_label = f'Before Fine-Tuning BART'
        after_label = f'Before Fine-Tuning DeBERTa'
    else:
        before_label = f'Before Fine-Tuning {name}'
        after_label = f'After Fine-Tuning {name}'
    return df_pre_ft, df_post_ft, before_label, after_label


def generate_histogram(position, interval_flag, pre_ft_values, post_ft_values, before_label, after_label):
    """
    Generates a histogram of the pre and post fine-tuning predictions.

    Args:
    - position (int): The position of the subplot (1 for left, 2 for right).
    - interval_flag (bool): If True, limits the x and y axes.
    """
    plt.subplot(1, 2, position)
    plt.hist(pre_ft_values, bins=50, alpha=0.7, label=before_label)
    plt.hist(post_ft_values, bins=50, alpha=0.7, label=after_label)
    plt.title('Histogram of Predictions')
    plt.xlabel('Prediction Values')
    plt.ylabel('Frequency')
    if interval_flag:
        plt.xlim(0.2, 1.0)
        plt.ylim(0, 100)
    plt.legend()


def generate_kernel(pre_ft_values, post_ft_values, before_label, after_label):
    """
    Generates a kernel density plot of the pre and post fine-tuning predictions.
    """
    # Dichte-Plots
    plt.subplot(1, 2, 2)
    sns.kdeplot(pre_ft_values, fill=True, label=before_label)
    sns.kdeplot(post_ft_values, fill=True, label=after_label)
    plt.title('Density Plot of Predictions')
    plt.xlabel('Prediction Values')
    plt.ylabel('Density')
    plt.ylim(0, 13)
    plt.legend()


def generate_histogram_and_kernel(name, path, comparison_path):
    """Generates both a histogram and a kernel density plot for the specified pre and post fine-tuning data."""
    plt.figure(figsize=(14, 6))
    df_pre_ft, df_post_ft, before_label, after_label = get_meta_data(name, path, comparison_path)
    pre_ft_values = df_pre_ft.values.flatten()
    post_ft_values = df_post_ft.values.flatten()

    generate_histogram(1, False, pre_ft_values, post_ft_values, before_label, after_label)
    generate_kernel(pre_ft_values, post_ft_values, before_label, after_label)


def generate_two_histograms():
    """Generates histograms comparing pre and post fine-tuning predictions for both BART and DeBERTa models."""
    plt.figure(figsize=(14, 6))
    df_pre_ft, df_post_ft, before_label, after_label = get_meta_data("BART", PRE_BART_PATH, POST_BART_PATH)
    pre_ft_values = df_pre_ft.values.flatten()
    post_ft_values = df_post_ft.values.flatten()
    generate_histogram(1, True, pre_ft_values, post_ft_values, before_label, after_label)

    df_pre_ft, df_post_ft, before_label, after_label = get_meta_data("DeBERTa", PRE_DEBERTA_PATH, POST_DEBERTA_PATH)
    pre_ft_values = df_pre_ft.values.flatten()
    post_ft_values = df_post_ft.values.flatten()
    generate_histogram(2, True, pre_ft_values, post_ft_values, before_label, after_label)


generate_histogram_and_kernel(None, PRE_BART_PATH, PRE_DEBERTA_PATH)
plt.tight_layout()
plt.show()

generate_histogram_and_kernel("BART", PRE_BART_PATH, POST_BART_PATH)
plt.tight_layout()
plt.show()

generate_histogram_and_kernel("DeBERTa", PRE_DEBERTA_PATH, POST_DEBERTA_PATH)
plt.tight_layout()
plt.show()

generate_two_histograms()
plt.tight_layout()
plt.show()
