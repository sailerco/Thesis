import MetricsGenerator as Metrics
import os

# generate metrics for given prediction files (csv)
directory = os.getcwd()
end_directory = os.path.join(directory, "output_csv")
path_endings = ['_08_3_1e-05_3232_0.1_0.06']
for i in path_endings:
    if '1e-05' in i:
        Metrics.MetricsGenerator(i, directory, end_directory, False, True, False).main()
    elif '2e-05' in i:
        Metrics.MetricsGenerator(i, directory, end_directory, False, False, True).main()