import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
import numpy as np

data = pd.read_csv("rel_canopy_h_time_since_burn_landcover", sep=" ", header=None, names=["canopy_heights", "time_since_last_burn", "landcover"])

lc_types = {3:["Forest_Formation"], 4:["Savannah_Formation"], 12:["Grassland"], 15:["Pasture"]}
data = data[data["landcover"].isin(lc_types.keys())].reset_index(drop=True)
data.time_since_last_burn = data.time_since_last_burn.astype(int)

## Convert yearly values to 5-year intervals
data["time_class"] = data["time_since_last_burn"]/5
data.time_class = data.time_class.astype(int)
xlabels = ["0-5", "5-10", "10-15", "15-20"]

## Getting normalized frequency for each combination of landcover and burn frequency
counts = data.groupby(["landcover", "time_class"])["canopy_heights"].count()
df_counts = pd.DataFrame([], columns=["landcover", "time_class", "count"], index=np.arange(0, counts.shape[0]))
for i in range(0 , df_counts.shape[0]):
   df_counts["landcover"][i] = counts.index[i][0]
   df_counts["time_class"][i] = counts.index[i][1]
   df_counts["count"][i] = counts.to_list()[i]
df_counts["normalized"] = df_counts["count"]/df_counts["count"].sum()

dict_time_class = {0:[[3,4,12,15], -0.25, 'mediumslateblue'], 1:[[3,4,12,15], -0.05, 'lime'], 2:[[3,4,12,15], 0.1, 'maroon'], 3:[[3,4,12,15], 0.2, 'olive']}

for i in dict_time_class.keys():
  for j in range(0, len(dict_time_class[i][0])):
     data_sub = data[(data["time_class"]==i) & (data["landcover"]==dict_time_class[i][0][j])].reset_index(drop=True)
     plt.boxplot(x = data_sub["canopy_heights"], positions = [j + dict_time_class[i][1]], whis=[5, 95],  patch_artist=True, boxprops=dict(facecolor=dict_time_class[i][2], color=dict_time_class[i][2]) , showfliers=False,
                 widths=df_counts[(df_counts["time_class"] == i) & (df_counts["landcover"] == dict_time_class[i][0][j])]["normalized"].to_list()[0])

plt.ylim(0,15)
plt.xticks(np.arange(0,4), ["Forest", "Savannah", "Grassland", "Pasture"], fontsize=8)
plt.yticks(np.arange(0,17.5,2.5), np.arange(0,17.5,2.5), fontsize=8)
plt.xlabel("Landcover type", fontsize=8, labelpad=10)
plt.ylabel("Relative canopy height (in m)", fontsize=8, labelpad=10)
plt.title("Relative canopy heights calculated over 30m along-track segments", fontsize=8)

legend_elements = [Patch(facecolor="mediumslateblue", edgecolor='mediumslateblue', label="0-5"),
                   Patch(facecolor="lime", edgecolor='lime', label="5-10"),
                   Patch(facecolor="maroon", edgecolor='maroon', label="10-15"),
                   Patch(facecolor="olive", edgecolor='olive', label="15-20")]
plt.legend(handles=legend_elements, loc='upper right', title="Years since last burn", fontsize=8, title_fontsize=8)
output_filename="boxplot_years_since_last_burn.png"
plt.savefig(output_filename, dpi=300)

#for i in lc_types.keys():
#   data_sub = data[data["landcover"] == i].reset_index(drop=True)
#   sns.boxplot(data_sub["time_since_last_burn"], data_sub["canopy_heights"], whis=[5,95], fliersize=0)
#   plt.ylim(0,20)
#   plt.xticks([0,1,2,3], xlabels, fontsize=10)
#   plt.xlabel("Years since last burn", fontsize=10, labelpad=10)
#   plt.yticks(np.arange(0, 25, 2.5), np.arange(0, 25, 2.5), fontsize=10)
#   plt.ylabel("Relative Canopy Heights (in m)", fontsize=10, labelpad=10)
#   plt.title("%s" %(lc_types[i][0]), fontsize=15, pad=15)
#   output_name = "boxplot_" + lc_types[i][0] + ".png"
#   plt.show()
#   #plt.savefig(output_name, dpi=300)
#   #plt.close()
