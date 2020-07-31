## Data for this is present at /data2/vk5/classification_results_may_2019 on mutiny
## This creates a plot for producer's and user's accuracy plot during the training period 2008-2014 in the paper

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv('accuracy_combined_ordered', sep=" ", header=None)
plt.rcParams['xtick.labelsize']=12
plt.rcParams['ytick.labelsize']=12

ax1 = sns.boxplot(x=data.iloc[:,4], y=data.iloc[:,1], data=data, color='white')
ax1 = sns.swarmplot(x=data.iloc[:,4], y=data.iloc[:,1], data=data, color=".25")
ax1.set_xticklabels(labels=('Corn','Soybeans','Winter Wheat','Fallow','Other Hay','Alfalfa','Sorghum','Rice'), fontsize=10, rotation=20)
ax1.set_title("Interannual Variability over 2008-2014", fontsize=12)
plt.ylabel("Producer Accuracy (%)", fontsize=12)
plt.ylim(25,85)
plt.savefig('multiyear_producer.png')
plt.close()

ax2 = sns.boxplot(x=data.iloc[:,4], y=data.iloc[:,2], data=data, color='white')
ax2 = sns.swarmplot(x=data.iloc[:,4], y=data.iloc[:,2], data=data, color=".25")
ax2.set_xticklabels(labels=('Corn','Soybeans','Winter Wheat','Fallow','Other Hay','Alfalfa','Sorghum','Rice'), fontsize=10, rotation=20)
ax2.set_title("Interannual Variability over 2008-2014", fontsize=12)
plt.ylim(25,85)
plt.ylabel("User's Accuracy (%)", fontsize=12)
plt.savefig('multiyear_user.png')
