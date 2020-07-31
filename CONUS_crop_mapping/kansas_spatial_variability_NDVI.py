## Data for this code is present at /data2/vk5/kansas_corn_analysis on mutiny
## This code creates the spatial variability in NDVI plot in Kansas 2013 used in the paper

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_1480 = np.loadtxt('r.stats_corn_2013_ndvi_phenoregion_1480')
data_4182 = np.loadtxt('r.stats_corn_2013_ndvi_phenoregion_4182')
output_1480 = np.empty(shape=(1,5))
output_4182 = np.empty(shape=(1,5))
for i in range(0,46):
  out_1480 = [np.percentile(data_1480[:,i],[5,25,50,75,95])]
  out_4182 = [np.percentile(data_4182[:,i],[5,25,50,75,95])]
  output_1480 = np.append(output_1480,out_1480,axis=0)
  output_4182 = np.append(output_4182,out_4182,axis=0)
percentiles_1480 = output_1480[1:,:]
percentiles_4182 = output_4182[1:,:]

plt.plot(np.arange(0,46), percentiles_1480[:,2],color='red')
plt.fill_between(np.arange(0,46),percentiles_1480[:,1], percentiles_1480[:,3], facecolor='red',alpha=0.3)
plt.fill_between(np.arange(0,46),percentiles_1480[:,0], percentiles_1480[:,4], facecolor='red',alpha=0.1)

plt.plot(np.arange(0,46), percentiles_4182[:,2],color='blue')
plt.fill_between(np.arange(0,46),percentiles_4182[:,1], percentiles_4182[:,3], facecolor='blue',alpha=0.3)
plt.fill_between(np.arange(0,46),percentiles_4182[:,0], percentiles_4182[:,4], facecolor='blue',alpha=0.1)

dates=pd.to_datetime(pd.Series(['20130101', '20130210','20130322','20130501','20130610','20130720','20130829','20131008','20131117','20131227']), format = '%Y%m%d')
dates_2=dates.apply(lambda x: x.strftime('%b-%d'))
plt.xticks(np.arange(0, 46, 5),dates_2, fontsize=12, rotation=30)
plt.yticks(fontsize=12)
plt.ylabel("NDVI", fontsize=12, labelpad=15)
plt.tight_layout()
plt.savefig('kansas_corn_analysis.png')
