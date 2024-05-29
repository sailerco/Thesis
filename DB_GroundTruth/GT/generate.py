import MetricsGenerator as Metrics
import os

dir = os.getcwd()
__file__ = "generate.py"
end_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ClassifierOutput'))
metrics = Metrics.MetricsGenerator("", dir, end_dir, False).main()
