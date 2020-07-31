## The data for this code is present at /data2/vk5/classification_results_may_2019 on mutiny
## This code creates a plot for producer's and user's accuracy for the test period 2015--2018 used in the paper

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("test_years_accuracy_combined", sep=" ", header=0)
#data = pd.read_csv("test_years_accuracy_combined_coarsened_cdl", header=None, sep=" ", names=["crop","prod","user","year"])
sns.set(style="whitegrid")
ax = sns.barplot(x="crop", y="prod", data=data, hue="year", order=[1,5,24,61,37,36,4,3])
labels=["Corn","Soybeans","Winter Wheat","Fallow","Other hay","Alfalfa","Sorghum","Rice"]
plt.ylim(30,80)
ax.set_xticklabels(labels, fontsize=10, rotation =19)
#ax.set_yticklabels([0,30,40,50,60,70,80])

plt.xlabel("")
plt.ylabel("Producer Accuracy (%)", fontsize=12, labelpad=12)
plt.legend(loc='best', fontsize=8.5, ncol=4)
plt.subplots_adjust(bottom=0.2)
#plt.savefig('testyear_producer_coarsened_cdl.png')
plt.savefig('testyear_producer.png')
plt.close()

ax2 = sns.barplot(x="crop", y="user", data=data, hue="year", order=[1,5,24,61,37,36,4,3])
labels=["Corn","Soybeans","Winter Wheat","Fallow","Other hay","Alfalfa","Sorghum","Rice"]
plt.ylim(30,70)
ax2.set_xticklabels(labels, fontsize=10, rotation =19)

plt.xlabel("")
plt.ylabel("User's Accuracy (%)", fontsize=12, labelpad=12)
plt.legend(loc='best', fontsize=8.5, ncol=4)
plt.subplots_adjust(bottom=0.2)
#plt.savefig('testyear_user_coarsened_cdl.png')
plt.savefig('testyear_user.png')
plt.close()
