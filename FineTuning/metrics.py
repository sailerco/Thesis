import MetricsGenerator as Metrics
import os
#new csv
dir = os.getcwd()
end_dir = os.path.join(dir, "output_csv")
for i in ["_06_result_after"]:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, True, False).main()

# old csv
#end_dir = dir
#for i in ["_08_result_after"]:
#    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, True, False).main()
