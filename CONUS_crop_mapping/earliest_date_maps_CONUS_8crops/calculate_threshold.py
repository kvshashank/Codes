import pandas as pd
import numpy as np
import os

os.chdir("/home/vk5/earliest_date_maps_CONUS_8crops/create_5pct_thresh_ecoregion_maps_8crops")

crops=[1,5,24,61,37,36,4,3]

eco_area = pd.read_csv("land_pixels_in_each_ecoregion", sep=" ", header=None, names=["ecoregion","pixels"])
eco_crop = pd.read_csv("ecoregionwise_crop_count", sep=" ", header=None, names=["ecoregion","crop","crop_pixels"])

# Subset 8 crops from the eco_crop file
eco_crop = eco_crop[eco_crop["crop"].isin(crops)]

# For each of the 8 crops create a file with a list of ecoregions with at least 5% area covered by that crop type
for crop in crops:
   data_sub = eco_crop[eco_crop["crop"] == crop].reset_index(drop=True)
   final = pd.DataFrame(data_sub, columns=["ecoregion","crop","crop_pixels","total_pixels","percent"], index=np.arange(0, len(data_sub))) 
   for i in range(0,len(data_sub)):
     final["total_pixels"][i] = eco_area[eco_area["ecoregion"] == data_sub["ecoregion"][i]]["pixels"]
     final["percent"][i] = (float(final["crop_pixels"][i])/final["total_pixels"][i])*100
   
   major_crop_eco = final[final["percent"]>5].reset_index(drop=True)
   output_name = "major_ecoregions_crop_" + str(crop) 
   major_crop_eco.to_csv(output_name, sep=" ", index=False, header=False)
