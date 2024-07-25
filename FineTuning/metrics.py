import MetricsGenerator as Metrics
import os

#new csv
dir = os.getcwd()
end_dir = os.path.join(dir, "old_output_csv")
"""for i in ["_08_contras", "_08_contras_ex_2epo", "_08_contras_ex_higherLR",
          "_08_contras_ex_higherLR_noWarm", "_08_contras_ex_higherLR_100Warm",
          "_08_contras_ex_higherLR_200Warm", "_08_contras_ex_higherLR_500Warm",
          "_08_contras_ex_higherLR_500Warm_1616", "_08_contras_ex_higherLR_500Warm_3216",
          "_08_contras_ex_new", "_06_contras_ex_simpleWithToken_2eLR_1ep", "_06_contras_ex_simple_2eLR_1ep"]:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, True, False).main()"""

"""for i in ["_06_1_5e-05_0.1_162", "_02_1_5e-05_0.1_162", "_02_1_1e-05_0.1_162_500_0.06_0.01",
          "_02_1_1e-05_0.1_162_50_0.1_0.01NOSMOOTH"]:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, True, False).main()"""

"""for i in [ '_02_3_2e-05_3232_0.1_0.06_exploded',
          '_08_3_2e-05_3232_0.1_0.06_exploded', '_08_6_2e-05_3232_0.1_0.06_exploded']:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, False, True).main()"""

#for i in [ '_08_3_2e-05_3232_0.1_0.06', '_08_6_2e-05_3232_0.1_0.06', '_08_10_2e-05_3232_0.1_0.06']:
#    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, False, True).main()

for i in [ '_08_freeze_3_2e-05_3232_0.1_0.06', '_08_freeze_6_2e-05_3232_0.1_0.06']:
    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, False, True).main()


#for i in [ '_08_3_1e-05_3232_0.1_0.06', '_08_6_1e-05_3232_0.1_0.06', '_08_10_1e-05_3232_0.1_0.06']:
#    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, True, False).main()

#for i in [ '_08_HP_3_1e-05_3232_0.1_0.06', '_08freeze_3_1e-05_3232_0.1_0.06', '_08freeze_6_1e-05_3232_0.1_0.06']:
#    metrics = Metrics.MetricsGenerator(i, dir, end_dir, False, True, False).main()