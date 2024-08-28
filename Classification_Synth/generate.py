import MetricsGenerator as Metrics
import os

directory = os.getcwd()
__file__ = "generate.py"
end_directory = os.path.join(directory, 'ClassifierOutput')
metrics = Metrics.MetricsGenerator("", directory, end_directory, False, False, True).main()
