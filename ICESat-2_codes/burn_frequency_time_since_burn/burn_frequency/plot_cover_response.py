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
burn_freq_dict = {0:["#fee5d9"], 1:['#fcae91'], 2:['#fb6a4a'], 3:['#de2d26'], 4:['#a50f15']}
custom_lines = [Patch(facecolor= "#fee5d9", edgecolor="black", label="0", linewidth=0.5), Patch(facecolor= "#fcae91", edgecolor="black", label="1", linewidth=0.5),
Patch(facecolor= "#fb6a4a", edgecolor="black", label="2", linewidth=0.5), Patch(facecolor= "#de2d26", edgecolor="black", label="3", linewidth=0.5), Patch(facecolor= "#a50f15", edgecolor="black", label=">=4", linewidth=0.5)]

fig, ax = plt.subplots(2,2, sharex=True, sharey=False)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.ylabel("Canopy cover (%)", labelpad=6, fontsize=8)
plt.xlabel("Precipitation zone", labelpad=6, fontsize=8)
plt.legend(handles=custom_lines, bbox_to_anchor = (0.8,-0.12), title="Burn frequency over 21 years", fontsize=8, title_fontsize=8, markerscale=0.6, ncol=6)

pos_dict = {3:[[-0.1, -0.045, -0.015, 0.005, 0.025], [0.9, 1.223, 1.298, 1.34, 1.385], [1.9, 2.01, 2.045, 2.075, 2.103]],
4:[[-0.1, -0.0019, 0.06, 0.105, 0.15], [0.9, 1.08, 1.15, 1.2, 1.265], [1.9, 1.975, 2.020879953620473, 2.055, 2.105]],
12:[[-0.1, -0.04, 0.01, 0.05, 0.09], [0.9, 1.0363, 1.1, 1.165, 1.3], [1.9, 1.942, 1.98, 2.016, 2.12]],
15:[[-0.1, -0.064, -0.049, -0.034, -0.022], [0.9, 1.292, 1.34, 1.362, 1.382], [1.9, 1.982, 2.01, 2.03, 2.05]]}

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
         
         pos = pos_dict[lc][j]
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
             slope = np.round(np.polyfit([0,1,2,3],median_list[0:4],1)[0], 2)

    ax[row, col].set_ylim(0,100)
    ax[row, col].set_yticks(np.arange(0,110,10))
    ax[row, col].set_yticklabels(np.arange(0,110,10), fontsize=8)
    ax[row, col].set_title(lc_dict[lc][0]+ " (%s)" %(str(lc_seg_count_w_commas)), fontsize=8)
    ax[row, col].set_xticks(np.arange(0,3))
    ax[row, col].set_xticklabels(["low", "med", "high"], fontsize=8)
    ax[row, col].grid(axis='y', color='lightgrey', linestyle='-', linewidth=1, alpha=0.5)
    for axis in ['top','bottom','left','right']:
       ax[row, col].spines[axis].set_linewidth(0.5)

ax[0,0].text(-0.4, 95, "-4.94 % burn$^{-1}$", fontsize=6)
ax[0,0].text(0.6, 95, "-0.67 % burn$^{-1}$", fontsize=6)
ax[0,0].text(1.6, 95, "-2.6 % burn$^{-1}$", fontsize=6)

ax[1,0].text(-0.4, 95, "-6.23 % burn$^{-1}$", fontsize=6)
ax[1,0].text(0.6, 95, "-5.08 % burn$^{-1}$", fontsize=6)
ax[1,0].text(1.6, 95, "-6.3 % burn$^{-1}$", fontsize=6)

ax[0,1].text(-0.4, 95, "-3.96 % burn$^{-1}$", fontsize=6)
ax[0,1].text(0.6, 95, "-3.75 % burn$^{-1}$", fontsize=6)
ax[0,1].text(1.6, 95, "-2.95 % burn$^{-1}$", fontsize=6)

ax[1,1].text(-0.4, 95, "-1.88 % burn$^{-1}$", fontsize=6)
ax[1,1].text(0.6, 95, "4.44 % burn$^{-1}$", fontsize=6)
ax[1,1].text(1.6, 95, "2.07 % burn$^{-1}$", fontsize=6)
plt.savefig("burn_freq_can_cover.png", dpi=300, bbox_inches="tight", pad_inches=0.1)
