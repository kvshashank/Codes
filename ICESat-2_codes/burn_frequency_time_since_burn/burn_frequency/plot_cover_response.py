import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

data = pd.read_csv("stratified_data_pcp_lc_burnfreq_canht_cancover_zero_transition_mask_nov28", sep=" ", header=None, names=["precip", "lc", "burn_freq", "can_ht", "can_cover"])
lc_dict = {3:["Forest"], 4: ["Savanna"], 12:["Grassland"], 15:["Pasture"]}
data = data[data["lc"].isin(lc_dict.keys())].reset_index(drop=True)
data["burn_freq"].replace(to_replace=np.arange(4,30,1), value=4, inplace=True)
groupby = data.groupby(["precip", "lc", "burn_freq"])["can_ht"].count()
df_groupby = groupby.reset_index()
df_groupby.columns = ["precip", "lc", "burn_freq", "count"]

### Normalize data for each lc type separately
df_normalized = pd.DataFrame([], columns=["normalized"], index=np.arange(0, len(df_groupby)))
df_groupby = pd.concat([df_groupby, df_normalized], axis=1)
for i in range(0, len(df_groupby)):
    lc = df_groupby["lc"][i]
    sum_segs = df_groupby[df_groupby["lc"] == lc]["count"].sum()
    df_groupby["normalized"][i] = df_groupby["count"][i]/sum_segs

lc_list = [3,4,12,15]
precip_class = [0,1,2]
burn_freq_dict = {0:['#2c7bb6'], 1:['#abd9e9'], 2:['#ffffbf'], 3:['#fdae61'], 4:['#d7191c']}
custom_lines = [Patch(facecolor= "#2c7bb6", edgecolor="black", label="0", linewidth=0.5), Patch(facecolor= "#abd9e9", edgecolor="black", label="1", linewidth=0.5),
Patch(facecolor= "#ffffbf", edgecolor="black", label="2", linewidth=0.5), Patch(facecolor= "#fdae61", edgecolor="black", label="3", linewidth=0.5), Patch(facecolor= "#d7191c", edgecolor="black", label=">=4", linewidth=0.5)]

fig, ax = plt.subplots(2,2, sharex=True, sharey=False)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.ylabel("Canopy cover (%)", labelpad=6, fontsize=8)
plt.xlabel("Precipitation zone", labelpad=6, fontsize=8)
plt.legend(handles=custom_lines, bbox_to_anchor = (0.8,-0.12), title="Burn frequency over 21 years", fontsize=8, title_fontsize=8, markerscale=0.6, ncol=6)

for i in range(0, len(lc_list)):
    lc = lc_list[i]
    row = i%2
    col = int(i/2)

    data_lc = data[data["lc"] == lc].reset_index(drop=True)
    lc_seg_count = data_lc.shape[0]
    lc_seg_count_w_commas = "{:,}".format(lc_seg_count)

    for j in precip_class:
         data_lc_precip = data_lc[data_lc["precip"] == j].reset_index(drop=True)
         normalized_vals = df_groupby[(df_groupby["precip"] == j) & (df_groupby["lc"] == lc)]["normalized"].to_list()
         
         ## Assign positions for boxplots
         pos = [j - 0.1, j - 0.1 + (1.1*normalized_vals[0])/2 + (1.1*normalized_vals[1])/2]
         for index in np.arange(1, len(burn_freq_dict) - 1):
             if ((normalized_vals[index] < 0.02) & (normalized_vals[index + 1] < 0.02)):
                 pos.append(pos[index] + (3*normalized_vals[index])/2 + (3*normalized_vals[index+1])/2)
             else:
                 pos.append(pos[index] + (1.7*normalized_vals[index])/2 + (1.7*normalized_vals[index+1])/2)

         ## Make boxplots
         line_props = dict(color="black", alpha=0.2)
         cap_props = dict(color="black", alpha=0.2)
         medians = data_lc_precip.groupby(["burn_freq"])["can_cover"].median()
         median_list = medians.tolist()
         for burn_freq in sorted(burn_freq_dict.keys()):
             data_lc_precip_bf = data_lc_precip[data_lc_precip["burn_freq"] == burn_freq].reset_index(drop=True)
             bp = ax[row, col].boxplot(x = data_lc_precip_bf["can_cover"], positions=[pos[burn_freq]], whis=[5,95], patch_artist=True, whiskerprops = line_props, capprops = cap_props,
                                 boxprops=dict(facecolor=burn_freq_dict[burn_freq][0], color=burn_freq_dict[burn_freq][0]), showfliers=False, widths=normalized_vals[burn_freq], medianprops=dict(linewidth=1))
             plt.setp(bp['medians'], color="black")
             #if all(k >= 0.004 for k in normalized_vals):
             slope = np.round(np.polyfit([0,1,2,3],median_list[0:4],1)[0], 2)
             ax[row, col].text(j-0.2, 0.3, slope, fontsize=8)

    ax[row, col].set_ylim(0,100)
    ax[row, col].set_yticks(np.arange(0,110,10))
    ax[row, col].set_yticklabels(np.arange(0,110,10), fontsize=8)
    ax[row, col].set_title(lc_dict[lc][0]+ " (%s)" %(str(lc_seg_count_w_commas)), fontsize=8)
    ax[row, col].set_xticks(np.arange(0,3))
    ax[row, col].set_xticklabels(["low", "med", "high"], fontsize=8)
    ax[row, col].grid(axis='y', color='lightgrey', linestyle='-', linewidth=1, alpha=0.5)
    for axis in ['top','bottom','left','right']:
       ax[row, col].spines[axis].set_linewidth(0.5)
plt.savefig("burn_freq_can_cover.png", dpi=300, bbox_inches="tight", pad_inches=0.1)
