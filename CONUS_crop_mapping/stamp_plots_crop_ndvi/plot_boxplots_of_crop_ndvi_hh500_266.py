import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

crop_names = pd.read_csv('crop_names',sep=",",header=None)

#uniq_crops=[1,2,3,4,5,23,24,26,36,37,43,61]
uniq_crops=[1,2]
fig_row = 4
fig_col = 3
f1, ax1 = plt.subplots(fig_row, fig_col,sharex=True,sharey=True,figsize=(20,10))                          # setting rows and columns for the subplots in the figure
f1.text(0.08, 0.5, 'NDVI', ha='center', va='center', rotation='vertical', fontsize=20)

for crop in uniq_crops:
    crop_index=uniq_crops.index(crop)
    print "working on crop number %d of %d" %(crop_index,len(uniq_crops))
    plot_row=int((crop_index)/fig_col)
    plot_col=crop_index%fig_col
    crop_data=pd.read_csv('r.stats_ecoregion_266_crop_%d_2008' % crop,sep=' ',header=None)
    num_pixels=crop_data.shape[0]
    num_hectares=(num_pixels*231*231)/10000
    num_hectares_str="{:,}".format(num_hectares)

    bp=ax1[plot_row,plot_col].boxplot(crop_data.as_matrix(),patch_artist=True,widths=0.2,whis=[5,95])
    for box in bp['boxes']:
        print(box[0])
    for box in bp['boxes']:
        box.set(color='#2e8b57',linewidth=2)
        box.set( facecolor = '#2e8b57' )
    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=0)
    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)
    for median in bp['medians']:
        median.set(color='#b22222', linewidth=2)
    for flier in bp['fliers']:
        flier.set(marker=' ', color='#e7298a', alpha=0)
    temp_name=crop_names[crop_names.iloc[:,0]==crop]
    crop_name=temp_name.iloc[0,1]

    ax1[plot_row,plot_col].set_title("%s (%s ha)" %(crop_name,num_hectares_str))               # setting titles and labels for the plot
    ax1[plot_row,plot_col].set_ylim([0,100])
    ax1[plot_row,plot_col].xaxis.set_ticks(np.arange(1, 47, 5))
    dates=pd.to_datetime(pd.Series(['20130101', '20130210','20130322','20130501','20130610','20130720','20130829','20131008','20131117','20131227']), format = '%Y%m%d')
    dates_2=dates.apply(lambda x: x.strftime('%b-%d'))
    ax1[plot_row,plot_col].xaxis.set_ticklabels(dates_2,rotation=45,fontsize=16)
plt.show()
#f1.savefig('ec_266_bp.png')
