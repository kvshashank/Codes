## This code calculates percent alder in each subwatershed and then plots the data
## The data for this analysis is available at /home/vk5/ngee_arctic/alder_upstream_downstream

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("kougarok_alder_count_each_subwatershed_for_sample_pts", sep=" ", header=None)

df = pd.DataFrame([], index=np.arange(0, len(data)), columns=["x_coord", "y_coord", "plant_comm", "percent_alder", 
                                                              "alder_area"])
for i in range(0, len(data)):
   df["x_coord"][i] = data.iloc[i,0]
   df["y_coord"][i] = data.iloc[i,1]
   df["plant_comm"][i] = data.iloc[i,2]
   df["percent_alder"][i] = np.round((data.iloc[i,3]/data.iloc[i,4])*100,2)
   df["alder_area"][i] = data.iloc[i,3]*25  ## calculate are in m^2

df.to_csv("kougarok_upstream_percent_and_area_alder", sep=" ", index=False)

ax = sns.boxplot(x="plant_comm", y="alder_area", data=df, whis=(5,95), showfliers=False, linewidth=0.5)
plt.yscale('log')
#ax.set_xticklabels(["Dry-Lic","Tuss-Lic",
#                  "Mix Shrb","Bir-Eric","Willow","Ald-Wil","Will-Bir",
#                  "Wet-Mead"], rotation=20)
ax.set_xticklabels(["Eric-Dwrf", "Tuss-Lic", "Bir-Eric", "Ald-Wil", "Wil-Bir", "Wet Mead", "Wet Sed"], rotation=20)

## Mention the number of samples
uniq_plant_comm = sorted(df["plant_comm"].unique())
for i in range(0,len(uniq_plant_comm)):
   plant_comm = uniq_plant_comm[i]
   n_samples = len(df[df["plant_comm"]==plant_comm].reset_index(drop=True))
   ax.text(i-0.3, (df[df["plant_comm"]==plant_comm]["alder_area"].quantile(q=0.95, interpolation="lower") + 100), "n=%d"%n_samples)

plt.ylim(1,max(df["alder_area"]))
plt.ylabel("Upstream Alder area ($m^2$)")
plt.xlabel("")
plt.title("Extended Council Watershed", fontsize=12)
ax.text(4,1000000,"whiskers represent \n $5^{th}$ and $95^{th}$ percentile")
plt.savefig("council_upstrm_ald_area.png")
