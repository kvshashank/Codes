import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as st
from matplotlib.lines import Line2D

pcp_class_types = ["low", "med", "high"]

plt.rcParams.update({'font.size': 8})
lc_types = [3, 4, 12, 15]
lc_dict = {3:["Forest"], 4:["Savannah"], 12:["Grassland"], 15:["Pasture"]}

fig, ax = plt.subplots(3,4, sharex=True, sharey=True)
fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.ylabel("Photon height above interpolated ground (in m)", labelpad=15)

colors = {0:["0", "#2c7bb6"], 1:["1", "#abd9e9"], 2:["2", "#ffffbf"], 3:["3", "#fdae61"], 4:[">= 4", "#d7191c"]}
custom_lines = [Line2D([0], [0], color= "#2c7bb6", label="0"), 
               Line2D([0], [0], color= "#abd9e9", label="1"),
               Line2D([0], [0], color= "#ffffbf", label="2"),
               Line2D([0], [0], color= "#fdae61", label="3"),
               Line2D([0], [0], color= "#d7191c", label=">=4")]

plt.legend(handles=custom_lines, bbox_to_anchor = (1.15,0.6), title="burn freq", fontsize=8)

for i in range(0, len(lc_types)):
     lc = lc_types[i]
     for j in range(0, len(pcp_class_types)):
         pcp_class = pcp_class_types[j]
         input_fname = "photon_data_lc_" + str(lc) + "_pcp_class_" + pcp_class  + "_burn_freq"
         data_sub = pd.read_csv(input_fname, sep=" ", header=None, names=["lc", "precip", "burn_freq", "ph_h"])
         lc_seg_count = data_sub.shape[0]
         lc_seg_count_w_commas = "{:,}".format(lc_seg_count)
         mn = 0
         mx = 20
         kde_xs = np.linspace(mn, mx, 80)
         for burn_freq in colors.keys():
             data_sub_burnfreq = data_sub[data_sub["burn_freq"]==burn_freq].reset_index(drop=True)
             kde = st.gaussian_kde(data_sub_burnfreq["ph_h"])
             ax[j,i].plot(kde.pdf(kde_xs), kde_xs, color=colors[burn_freq][1], label=colors[burn_freq][0])
             ax[j,i].set_yticks(np.arange(0, 15, 2))
             ax[j,i].set_yticklabels(np.arange(0, 15, 2))
             ax[j,i].set_xticks(np.arange(0, 0.9, 0.2))
             xticklab = []
             for x in np.arange(0, 0.9, 0.2):
                 xticklab.append(np.round(x,2))
             ax[j,i].set_xticklabels(xticklab)
             ax[j,i].set_ylim(0, 12)
             ax[j,i].set_xlim(0, 0.7)
             ax[j,i].text(0.1,11,"n_ph = %s" %(lc_seg_count_w_commas), fontsize=6)
         if j==0:
            ax[j,i].set_title(lc_dict[lc][0])
         if i==0:
            ax[j,i].set_ylabel(pcp_class + " precip") 
plt.title("Impact of burn frequency on canopy height (night time data only)", pad=20)
plt.savefig("waveform_plot_burn_freq.png", dpi=300)
