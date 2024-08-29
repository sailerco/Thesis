import MetricsGenerator as Metrics
import os
"""
    generate metrics for the predicted values. The predictions are saved as csv's in the final_assets/output_csv folder
"""

dir = os.getcwd()
__file__ = "generate.py"
end_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'final_assets', 'output_csv'))
for i in ["_removed", "_grouped", "_removed_grouped"]:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, True, True, True).main()
