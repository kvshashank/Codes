import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.interpolate import CubicSpline
import os

def threshold_doy(ecoregion_data):
   eco = int(ecoregion_data[0,2])
   full_season_acc = ecoregion_data[ecoregion_data[:,3]==46,1]
   min_acc = min(ecoregion_data[:,1])
   target_acc = max(0.9*full_season_acc, min_acc) + 0.001

   for i in range(0, len(ecoregion_data)):
      if (ecoregion_data[i,1]-target_acc) > 0:
          break

   index = (np.abs(ecoregion_data[0:(i+1),1]-target_acc)).argmin()
   init_val = ecoregion_data[index,3]

   spline_fit = CubicSpline(ecoregion_data[:,3], ecoregion_data[:,1], axis=1)
   spline_fit2 = lambda x: spline_fit(x) - target_acc
   target_date = optimize.newton(spline_fit2, init_val, maxiter=100, tol=0.05)
   doy = int(target_date*8)
   print(eco,init_val,target_date,doy)
   return(doy)

crops=[1,5,24,61,37,36,4,3]

for crop in crops:
  os.chdir("/home/vk5/earliest_date_maps_CONUS_8crops/crop_" + str(crop))
  input_file="accuracy_2015_crop_" + str(crop) + "_user_acc"
  data = pd.read_csv(input_file, sep=" ", header=None, names=["crop","user_acc","ecoregion","interval"])
  data = data.sort_values(by=["ecoregion"])
  
  greenup = pd.read_csv("ecoregionwise_avg_greenup_crop_" + str(crop), header=None, sep=" ", names=["ecoregion","greenup","nearest_greenup"])
  ecoregions = greenup["ecoregion"].to_list()
  
  ## Output a table with ecoregion_no, threshold_doy_corn/soy
  output = pd.DataFrame([], index=np.arange(0, len(ecoregions)), columns=["ecoregion","threshold_doy"])
  
  ## Pick 1 ecoregion at a time
  for j in range(0, len(output)):
      output["ecoregion"][j] = ecoregions[j]
      nearest_greenup = int(greenup[greenup["ecoregion"] == ecoregions[j]]["nearest_greenup"])
      ecoregion_data = data[data["ecoregion"] == ecoregions[j]].reset_index(drop=True)
      ecoregion_data = ecoregion_data.sort_values(by=["interval"])
      ecoregion_data = ecoregion_data[ecoregion_data["interval"] >= nearest_greenup]
      output["threshold_doy"][j] = threshold_doy(np.array(ecoregion_data))
  
  output_file = "crop_" + str(crop) + "_ecoregion_doy_thresholds_2015" 
  output.to_csv(output_file, sep=" ", header=False, index=False)
