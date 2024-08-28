import os

import MetricsGenerator as Metrics

"""
    Generate Metrics Table
"""

PATH_ENDINGS = ['_all_labels_6Eps']
DEFAULT_TRUTH_DIR_PATH = False
GENERATE_METRIC_FOR_BART = True
GENERATE_METRIC_FOR_DEBERTA = True

# Get current directory and set end directory
BASE_DIR = os.getcwd()
END_DIR = os.path.join(BASE_DIR, "PostFineTuning")


def get_classification_metrics():
    # Loop through path endings and generate metrics for each
    for path_ending in PATH_ENDINGS:
        metrics_generator = Metrics.MetricsGenerator(
            path_ending,
            BASE_DIR,
            END_DIR,
            DEFAULT_TRUTH_DIR_PATH,
            GENERATE_METRIC_FOR_BART,
            GENERATE_METRIC_FOR_DEBERTA
        )
        metrics_generator.main()


get_classification_metrics()
