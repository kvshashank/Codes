import pandas as pd
import numpy as np
import os
crops=[1,5,24,61,37,36,4,3]

for crop in crops:
  dir_name = "crop_" + str(crop)
  os.chdir("/home/vk5/earliest_date_maps_CONUS_8crops/" + dir_name)
  data = pd.read_csv("ecoregionwise_crop_" + str(crop) + "_pixel_greenup", header=None, sep=" ", names=["ecoregion","greenup_interval","count"])
  ecoregions = data["ecoregion"].unique()
  nearest_greenup = np.arange(12,44,4)
  nearest_greenup = np.append(nearest_greenup, [43,46])
  
  output= pd.DataFrame([],columns=["ecoregion","greenup","nearest_interval"], index=np.arange(0, len(ecoregions)))
  for i in range(0, len(ecoregions)):
     output["ecoregion"][i] = ecoregions[i]
     
     subset = data[data["ecoregion"]==ecoregions[i]].reset_index(drop=True)
     avg_num = np.dot(subset["greenup_interval"], subset["count"])
     avg_denom = subset["count"].sum()
     avg_greenup = avg_num/avg_denom
     output["greenup"][i] = avg_greenup
     output["nearest_interval"][i] = min(nearest_greenup[(nearest_greenup - avg_greenup) > 0])
  
  file_name="ecoregionwise_avg_greenup_crop_" + str(crop) 
  output.to_csv(file_name, header=None, sep=" ", index=False)
