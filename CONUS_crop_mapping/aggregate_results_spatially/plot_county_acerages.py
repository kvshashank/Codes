## The data for this code is present at /home/vk5/aggregate_results_spatially/obs_vs_pred_scatterplot/obs_pred_county on theseus

import numpy as np
import matplotlib.pyplot as plt
import os, glob
from scipy import stats
import seaborn as sns
from sklearn.metrics import mean_squared_error
from math import sqrt

predict = np.loadtxt(fname='r.stats_2015_county_reclassed_pheno_count_8crops', dtype=float, delimiter=" ")
obs = np.loadtxt(fname='r.stats_2015_county_cdl_count_8crops', dtype=float, delimiter=" ")

print(predict[0:5,:])
