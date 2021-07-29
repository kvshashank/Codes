import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import scipy

data = pd.read_csv("rel_canopy_heights_burn_freq_landcover_strat", sep=" ", header=None, names=["rel_canopy_height", "burn_freq", "landcover"])

## Pick only 4 landcover classes: Grasslands (12), Savannahs (4), Pasture (15) and Forests (3)
data = data[(data["landcover"]==3) | (data["landcover"]==4) | (data["landcover"]==12) | (data["landcover"]==15)].reset_index(drop=True)

burn_class = pd.DataFrame([], columns=["burn_class"], index=np.arange(0, len(data)))
data = pd.concat([data, burn_class], axis=1)

data.loc[data["burn_freq"]>=20, ["burn_class"]] = 4
data.loc[data["burn_freq"]<20, ["burn_class"]] = data["burn_freq"]/5
data["burn_class"] = data["burn_class"].astype("int")
data["landcover"] = data["landcover"].astype("int")

## Getting normalized frequency for each combination of landcover and burn frequency
counts = data.groupby(["landcover", "burn_class"])["rel_canopy_height"].count()
df_counts = pd.DataFrame([], columns=["landcover", "burn_class", "count"], index=np.arange(0, counts.shape[0]))
for i in range(0 , df_counts.shape[0]):
   df_counts["landcover"][i] = counts.index[i][0]
   df_counts["burn_class"][i] = counts.index[i][1]
   df_counts["count"][i] = counts.to_list()[i]
df_counts["normalized"] = df_counts["count"]/df_counts["count"].sum()

dict_burn_class = {0:[[3,4,12,15], -0.25, 'blue'], 1:[[3,4,12,15], -0.05, 'green'], 2:[[3,4,12,15], 0.1, 'yellow'], 3:[[3,4,12], 0.2, 'red']}

for i in dict_burn_class.keys():
  for j in range(0, len(dict_burn_class[i][0])):
     data_sub = data[(data["burn_class"]==i) & (data["landcover"]==dict_burn_class[i][0][j])].reset_index(drop=True)
     plt.boxplot(x = data_sub["rel_canopy_height"], positions = [j + dict_burn_class[i][1]], whis=[5, 95],  patch_artist=True, boxprops=dict(facecolor=dict_burn_class[i][2], color=dict_burn_class[i][2]) , showfliers=False, 
                 widths=df_counts[(df_counts["burn_class"] == i) & (df_counts["landcover"] == dict_burn_class[i][0][j])]["normalized"].to_list()[0])

plt.ylim(0,15)
plt.xticks(np.arange(0,4), ["Forest", "Savannah", "Grassland", "Pasture"], fontsize=8)
plt.yticks(np.arange(0,17.5,2.5), np.arange(0,17.5,2.5), fontsize=8)
plt.xlabel("Landcover type", fontsize=8, labelpad=10)
plt.ylabel("Relative canopy height (in m)", fontsize=8, labelpad=10)
plt.title("Relative canopy heights calculated over 30m along-track segments", fontsize=8)

legend_elements = [Patch(facecolor="blue", edgecolor='b', label="0-4"), 
                   Patch(facecolor="green", edgecolor='g', label="5-9"),
                   Patch(facecolor="yellow", edgecolor='y', label="10-14"),
                   Patch(facecolor="red", edgecolor='r', label="15-19")]
plt.legend(handles=legend_elements, loc='upper right', title="20-yr burn frequency", fontsize=8, title_fontsize=8)
output_filename="low_burn_vs_high_burn_heights_jul27.png"
plt.savefig(output_filename, dpi=300)

########## Calculate sample size for each box and plot it right above the median ##################
#medians = data.groupby(["landcover", "burn_high_low"])["canopy_heights"].median()
#counts = data.groupby(["landcover", "burn_high_low"])["canopy_heights"].count()
#ptile_95 = data.groupby(["landcover", "burn_high_low"])["canopy_heights"].quantile(q=0.95)
#
#df = pd.DataFrame([], columns=["landcover", "burn_high_low", "median", "count", "ptile_95"], index=np.arange(0, medians.shape[0]))
#for i in range(0 , df.shape[0]):
#  df["landcover"][i] = medians.index[i][0]
#  df["burn_high_low"][i] = medians.index[i][1]
#  df["median"][i] = medians.to_list()[i]
#  df["count"][i] = counts.to_list()[i]
#  df["ptile_95"][i] = ptile_95.to_list()[i]
#
#uniq_landcover = df["landcover"].unique()
#
#for i in range(0, len(uniq_landcover)):
#    lc = uniq_landcover[i]
#    df_sub = df[df["landcover"]==lc].reset_index(drop=True)
#    plt.text(x = i - 0.4, y = df_sub[df_sub["burn_high_low"] == "low"]["median"].to_list()[0] + 0.5, s = "n=%d" %(df_sub[df_sub["burn_high_low"] == "low"]["count"].to_list()[0]), fontsize=6)
#    plt.text(x = i + 0.05, y = df_sub[df_sub["burn_high_low"] == "high"]["median"].to_list()[0] + 0.5, s = "n=%d" %(df_sub[df_sub["burn_high_low"] == "high"]["count"].to_list()[0]), fontsize=6)
#
#    ## Perform test for statistical significance 
#    res = scipy.stats.mannwhitneyu(x=data[(data["burn_high_low"] == "low") & (data["landcover"] == lc)]["canopy_heights"], y=data[(data["burn_high_low"] == "high") & (data["landcover"] == lc)]["canopy_heights"], alternative='two-sided') 
#    plt.text(x = i - 0.2, y = df_sub[df_sub["burn_high_low"] == "low"]["ptile_95"].to_list()[0] + 0.5, s = "p-value=%.2e" %(res.pvalue), fontsize=6)
#
#output_filename="low_burn_vs_high_burn_heights.png"
#plt.savefig(output_filename, dpi=300)
