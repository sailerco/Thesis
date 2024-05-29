import MetricsGenerator as Metrics
import os

dir = os.getcwd()
__file__ = "generate.py"
end_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'final_assets', 'Output'))
for i in ["_removed"]:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, True).main()
