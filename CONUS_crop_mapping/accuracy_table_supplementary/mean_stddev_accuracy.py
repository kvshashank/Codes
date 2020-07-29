# This code creates a table with the columns "Crop" "CONUS_wide_acreage" "Min_User's Acc" "Max User's Acc"  "User's Accuracy Weighted_avg" "User's Acc Weighted Std Dev"
## This table went in to the supplementary of the paper
## The data for this code is present at /home/vk5/ecoregionwise_overall_acc on theseus

import pandas as pd
import numpy as np
from math import sqrt

data = pd.read_csv("ecoregionwise_crop_accuracy", sep=" ", header=None, names=["Ecoregion", "Crop", "no._of_pixels", "user's_acc"])
data = data[(data["Crop"]<=77) | (data["Crop"]>=204)]

crop_names = pd.read_csv("crop_names", sep="\t", header=0, names=["Value", "Category"])
crop_names = crop_names.dropna()
data = data[data["Crop"].isin(crop_names["Value"])]

uniq_crops = data["Crop"].unique()

output = pd.DataFrame([], index=np.arange(0,len(uniq_crops)), columns=["Crop_Name", "CONUS_Acreage", "Min", "Max", "Weighted Average", "Weighted Std Dev."])

def wtd_std_dev(df, wm):
   num = 0
   denom = 0
   for j in range(0, len(df)):
      num = num + df["no._of_pixels"][j]*(df["user's_acc"][j] - wm)**2
      denom = denom + df["no._of_pixels"][j]
   factor = len(df)/(len(df) - 1)
   wtd_std_dev = sqrt(factor * (num/denom))
   return(wtd_std_dev)


for i in range(0,len(uniq_crops)):
  crop = uniq_crops[i]
  output["Crop_Name"][i] = crop_names[crop_names["Value"] == crop]["Category"].reset_index(drop=True)[0]
  
  # Subset rows belonging to that particular crop type from data
  data_sub = data[data["Crop"]==crop].reset_index(drop=True)
  
  # Calculate CONUS-wide acreage
  total_crop_pixel = data_sub["no._of_pixels"].sum()
  crop_area = (total_crop_pixel)*30*32/1000000  ## in km^2
  output["CONUS_Acreage"][i] = crop_area

  # Calculate Min/Max
  output["Min"][i] = min(data_sub["user's_acc"])
  output["Max"][i] = max(data_sub["user's_acc"])

  # Weighted Average
  output["Weighted Average"][i] = np.average(data_sub["user's_acc"], weights=data_sub["no._of_pixels"]) 

  # Weighted Std Dev
  if len(data_sub) > 1:
     output["Weighted Std Dev."][i] = wtd_std_dev(data_sub, output["Weighted Average"][i])
 
output = output.sort_values(by=["CONUS_Acreage"], ascending=False).reset_index(drop=True)
output.to_csv("accuracy_stats_100_crops_CONUS", sep=" ", index=False)
