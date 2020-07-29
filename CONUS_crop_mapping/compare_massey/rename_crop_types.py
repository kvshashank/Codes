## This code combines certain crop categories together so as to compare with the results from Massey et al. 2017
## The data for this is available at /home/vk5/compare_massey

import pandas as pd
import numpy as np

data = pd.read_csv("r.stats_phenoregion_cdl_2008", sep=" ", header=None, names=["predicted", "cdl", "count"])
new_crop_def = {1:[5], 24:[22,23], 36:[37]}
for key, values in new_crop_def.items():
     data["predicted"].replace(values, key, inplace=True)
     data["cdl"].replace(values, key, inplace=True)

uniq_rows = np.unique(data[["predicted", "cdl"]], axis=0)
new_data = pd.DataFrame([],columns=data.columns,index=np.arange(0,len(uniq_rows)))

for i in range(0, len(uniq_rows)):
   new_data["predicted"][i] = uniq_rows[i,0]
   new_data["cdl"][i] = uniq_rows[i,1]
   new_data["count"][i] = data[(data["predicted"] == uniq_rows[i,0]) & (data["cdl"] == uniq_rows[i,1])]["count"].sum() 

new_data.to_csv("r.stats_phenoregion_cdl_combined_crops_classes", sep=" ", header=False, index=False)
