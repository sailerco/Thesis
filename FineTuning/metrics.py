import MetricsGenerator as Metrics
import os

dir = os.getcwd()
end_dir = dir
for i in ["_09_result_after"]:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False).main()
