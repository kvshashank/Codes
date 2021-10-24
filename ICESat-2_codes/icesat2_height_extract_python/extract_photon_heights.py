import pandas as pd
import h5py
import numpy as np
import os, glob

year=2018
os.chdir("/home/vk5/postdoc/ATL08_cerrado/" + str(year))

for h5 in sorted(glob.glob("ATL08_*.h5")):
   print("working on %s" %h5)
   os.chdir("/home/vk5/postdoc/ATL08_cerrado/" + str(year))
   f = h5py.File(h5, "r")
   filename_pattern = h5.split("_")[1]
   month = int(filename_pattern[4:6])
   os.chdir("/home/vk5/postdoc/ATL03_cerrado/" + str(year))
   atl03_filename = glob.glob("ATL03_" + filename_pattern + "_*.h5")[0]
   f_atl03 = h5py.File(atl03_filename, "r")
   
   orient = pd.DataFrame(f["orbit_info/sc_orient"][:]).iloc[0,0]
   if orient==0:  ### Backward orientation -- strong beam is on the left side
     dir = "l"
   elif orient==1:   ### Forward orientation -- strong beam is on the right side
     dir = "r"
   
   beams = ["gt1" + dir, "gt2" + dir, "gt3" + dir]
   
   for beam in beams:
      ######## ATL08 data #########
      photon_classify = pd.DataFrame(f[beam + "/signal_photons/classed_pc_flag"][:]) #0:noise, 1:ground, 2:canopy, 3:top_of_canopy
      d_flag = pd.DataFrame(f[beam + "/signal_photons/d_flag"][:]) # 0:noise, 1:signal
      delta_time =  pd.DataFrame(f[beam + "/signal_photons/delta_time"][:])  # 
      ph_h = pd.DataFrame(f[beam + "/signal_photons/ph_h"][:])  # Height above interpolated ground surface at the location of the photon
      ph_segment_id = pd.DataFrame(f[beam + "/signal_photons/ph_segment_id"][:])  ## 20m segment id 
      df = pd.concat([photon_classify, d_flag, delta_time, ph_h, ph_segment_id], axis=1)
      df.columns=["photon_classify", "d_flag", "delta_time", "ph_h", "segment_id"]
      df = df[(df["photon_classify"] > 0) & (df["d_flag"] > 0)].reset_index(drop=True)
     
      ######## ATL03 data ##########
      atl03_seg_id = pd.DataFrame(f_atl03[beam + "/geolocation/segment_id"][:])
      atl03_lat = pd.DataFrame(f_atl03[beam + "/geolocation/reference_photon_lat"][:])
      atl03_lon = pd.DataFrame(f_atl03[beam + "/geolocation/reference_photon_lon"][:])
      df_atl03 = pd.concat([atl03_seg_id, atl03_lat, atl03_lon], axis=1)
      df_atl03.columns = ["segment_id", "lat", "lon"]
      df_atl03 = df_atl03[(df_atl03["lat"] > -25) & (df_atl03["lat"] < -2)].reset_index(drop=True)
      
      ####### Merge ATL08 and ATL03 dataframes
      merge_df = df.merge(df_atl03, how="inner", on="segment_id")
      merge_df = merge_df.dropna()
      merge_df = merge_df.drop(["d_flag", "delta_time"], axis=1)
      
      ####### Extract data quality info from ATL08 ############
      water_mask = pd.DataFrame(f[beam + "/land_segments/segment_watermask"][:], columns=[""]) ## 0 is no water, 1 is water. Derived from 250m water mask.
      urban_mask = pd.DataFrame(f[beam + "/land_segments/urban_flag"][:], columns=[""]) ## 0 is not urban; 1 is urban
      #canopy_rh_conf = pd.DataFrame(f[beam + "/land_segments/canopy/canopy_rh_conf"][:], columns=[""]) ## 2 is good
      cloud_flag_atm = pd.DataFrame(f[beam + "/land_segments/cloud_flag_atm"][:], columns=[""]) ## 0 is good
      ph_removal_flag =  pd.DataFrame(f[beam + "/land_segments/ph_removal_flag"][:], columns=[""]) ## True is bad(greater than 50% photons removed)
      seg_id_begin =  pd.DataFrame(f[beam + "/land_segments/segment_id_beg"][:], columns=[""])
      day_night = pd.DataFrame(f[beam + "/land_segments/night_flag"][:], columns=[""])
      seg_id_end = pd.DataFrame(f[beam + "/land_segments/segment_id_end"][:], columns=[""])
      #df_quality = pd.concat([water_mask, urban_mask, canopy_rh_conf, cloud_flag_atm, ph_removal_flag, seg_id_begin, seg_id_end, day_night], axis=1)
      df_quality = pd.concat([water_mask, urban_mask, cloud_flag_atm, ph_removal_flag, seg_id_begin, seg_id_end, day_night], axis=1)
      #df_quality.columns = ["water_mask","urban_mask","canopy_rh_conf","cloud_flag_atm","ph_removal_flag","seg_id_begin","seg_id_end", "day_night"]
      #df_quality = df_quality[(df_quality["water_mask"]==0) & (df_quality["urban_mask"]==0) & (df_quality["canopy_rh_conf"]==2) & 
      #                        (df_quality["cloud_flag_atm"] == 0) & (df_quality["ph_removal_flag"] == 0)].reset_index(drop=True)
      df_quality.columns = ["water_mask","urban_mask","cloud_flag_atm","ph_removal_flag","seg_id_begin","seg_id_end", "day_night"]
      df_quality = df_quality[(df_quality["water_mask"]==0) & (df_quality["urban_mask"]==0) &
                              (df_quality["cloud_flag_atm"] == 0) & (df_quality["ph_removal_flag"] == 0)].reset_index(drop=True)      

      valid_segs = pd.DataFrame([], index=np.arange(0,1), columns=["segment_id", "day_night"])
      for i in range(0, len(df_quality)):
         temp = pd.DataFrame([], index=np.arange(0,5), columns=["segment_id", "day_night"])
         for j in range(0, 5):
            temp["segment_id"][j] = df_quality["seg_id_begin"][i] + j
            temp["day_night"][j] = df_quality["day_night"][i] 
         valid_segs = valid_segs.append(temp, ignore_index=True)
      valid_segs = valid_segs.dropna()     
      
      ########### Select only those segments which are clean ############
      merge_df = merge_df[merge_df["segment_id"].isin(valid_segs["segment_id"])].reset_index(drop=True)
      #### Add day night information 
      merge_df = merge_df.merge(valid_segs, how="inner", on="segment_id")
      #### Add month
      merge_df["month"] = month
      #### Add file id 
      output = pd.concat([merge_df["lat"], merge_df["lon"], merge_df["segment_id"], merge_df["ph_h"], merge_df["photon_classify"], merge_df["day_night"], merge_df["month"]], axis=1)
      os.chdir("/home/vk5/postdoc/calculate_recovery/photon_data_extraction")
      output.to_csv("photon_data_" + filename_pattern + "_" + beam + ".csv", sep=" ", header=None, index=None)
