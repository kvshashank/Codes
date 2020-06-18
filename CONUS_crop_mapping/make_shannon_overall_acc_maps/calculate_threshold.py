## This code finds ecoregions within CONUS which have at least 20% of their area covered by crop cover
## This threshold method is needed for making Shannon entropy maps and overall accuracy maps 
## The data for this code is available /home/vk5/remake_overall_acc_shannon_maps on theseus machine

import pandas as pd
import numpy as np

eco_area = pd.read_csv("ecoregion_pixels", sep=" ", header=None, names=["ecoregion","pixels"])
eco_crop = pd.read_csv("crop_pixels_in_every_ecoregion", sep=" ", header=None, names=["ecoregion","crop","crop_pixels"])

final = pd.DataFrame(eco_crop, columns=["ecoregion","crop","crop_pixels","total_pixels","percent"], index=np.arange(0, len(eco_crop)))

for i in range(0,len(eco_crop)):
   final["total_pixels"][i] = eco_area[eco_area["ecoregion"] == eco_crop["ecoregion"][i]]["pixels"]
   final["percent"][i] = (float(final["crop_pixels"][i])/final["total_pixels"][i])*100

major_crop_eco = final[final["percent"]>=20].reset_index(drop=True)
#print(len(major_crop_eco))
major_crop_eco.to_csv("major_crop_eco_20pct_thresh", sep=" ", index=False)
