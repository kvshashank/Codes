## Data for this code is present at /data2/vk5/stamp_plots_crop_ndvi on mutiny
## This code creates stamp plots of ndvi profiles used in the paper

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

crops=[1,2,3,4,5,23,24,26,36,37,43,61]
fig_row = 4
fig_col = 3
fig, ax1 = plt.subplots(fig_row, fig_col,sharex=True,figsize=(20,10)) 
#f1.text(0.08, 0.5, 'NDVI', ha='center', va='center', rotation='vertical', fontsize=15)
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.ylabel("NDVI", fontsize=20, labelpad=25)

crop_names = pd.read_csv('crop_names',sep=",",header=None)

for crop in crops:
   data = np.loadtxt('r.stats_eco_266_crop_%d_5years'%crop)
   output=np.empty(shape=(1,5))
   for i in range(0,46):
      out = [np.percentile(data[:,i],[5,25,50,75,95])]
      output = np.append(output,out,axis=0)
   percentiles = output[1:,:]
   
   crop_index=crops.index(crop)
   print "working on crop %d" %(crop)
   plot_row=int((crop_index)/fig_col)
   plot_col=crop_index%fig_col
   num_pixels=data.shape[0]
   num_hectares=(num_pixels*231*231)/10000
   num_hectares_str="{:,}".format(num_hectares)
   temp_name=crop_names[crop_names.iloc[:,0]==crop]
   crop_name=temp_name.iloc[0,1]

   ax1[plot_row,plot_col].plot(np.arange(0,46), percentiles[:,2],color='green',alpha=0.3)
   ax1[plot_row,plot_col].fill_between(np.arange(0,46),percentiles[:,1], percentiles[:,3], facecolor='green',alpha=0.3)
   ax1[plot_row,plot_col].fill_between(np.arange(0,46),percentiles[:,0], percentiles[:,4], facecolor='green',alpha=0.1)
   ax1[plot_row,plot_col].set_title("%s (%s ha)" %(crop_name,num_hectares_str), fontsize=20)
   ax1[plot_row,plot_col].set_ylim([0,100])
   ax1[plot_row,plot_col].yaxis.set_ticks(np.arange(0,120,20))
   ax1[plot_row,plot_col].yaxis.set_ticklabels(np.arange(0,120,20),fontsize=14)
   ax1[plot_row,plot_col].xaxis.set_ticks(np.arange(0, 46, 5))
   dates=pd.to_datetime(pd.Series(['20130101', '20130210','20130322','20130501','20130610','20130720','20130829','20131008','20131117','20131227']), format = '%Y%m%d')
   dates_2=dates.apply(lambda x: x.strftime('%b-%d'))
   ax1[plot_row,plot_col].xaxis.set_ticklabels(dates_2,rotation=45,fontsize=16)
plt.tight_layout()
plt.savefig("crop_specific_ndvi.png")
