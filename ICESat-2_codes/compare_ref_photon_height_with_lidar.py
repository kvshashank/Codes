import os, h5py
import pandas as pd
import numpy as np
import glob
import pyproj

atl08 = pd.read_csv("ATL08_shortlisted_segments.csv", header=0)
atl08 = atl08[atl08["h_canopy_uncertainty"]<5].reset_index(drop=True)

## Create a list of 20-m segment ids 
seg_20m_list = []
for i in range(0, len(atl08)):
    for j in range(int(atl08["seg_id_begin"][i]), int(atl08["seg_id_end"][i] + 1)):
        seg_20m_list.append(j) 

beam_numbers = ['/gt1r', '/gt2r', '/gt3r']

## Select h5 filenames
h5_names = []
os.chdir('/home/vk5/icesat_2/ATL03_data')
for filename in sorted(glob.glob("*.h5")):
  h5_names.append(filename.split("_")[1:])

## Final output file
output = pd.DataFrame([], columns=["reference_ph_lat", "reference_ph_lon", "ph_height"])

## Select ATL03 and ATL08 data for each h5 filename
for j in range(0, len(h5_names)):
   print("working on %d of %d files" %(j, len(h5_names)))  
 
   ### ATL03 data
   os.chdir('/home/vk5/icesat_2/ATL03_data')
   filename = "ATL03_" + h5_names[j][0] + "_" + h5_names[j][1] + "_" + h5_names[j][2] + "_" + h5_names[j][3]
   f = h5py.File(filename, 'r')
   atl03_photon_data = pd.DataFrame([], columns=["reference_ph_lat", "reference_ph_lon", "segment_id",
                                                "index_within_seg"])   

   for beam in beam_numbers:
      ref_ph_index_within_seg = pd.DataFrame(f[beam + '/geolocation/reference_photon_index'][:])
      ref_ph_lat = pd.DataFrame(f[beam + '/geolocation/reference_photon_lat'][:])
      ref_ph_lon = pd.DataFrame(f[beam + '/geolocation/reference_photon_lon'][:])
      seg_id = pd.DataFrame(f[beam + '/geolocation/segment_id'][:])
      
      ## Combine reference photon information
      ref_ph = pd.concat([ref_ph_lat, ref_ph_lon, seg_id, ref_ph_index_within_seg], axis=1)
      ref_ph.columns = atl03_photon_data.columns
      
      ## Extract only those 20-m segment ids which exist in atl08 shortlist 
      ref_ph = ref_ph[ref_ph["segment_id"].isin(seg_20m_list)].reset_index(drop=True)
      
      atl03_photon_data = atl03_photon_data.append(ref_ph, ignore_index=True)
 
  
   ### ATL08 data
   os.chdir('/home/vk5/icesat_2/ATL08_data')
   filename = "ATL08_" + h5_names[j][0] + "_" + h5_names[j][1] + "_" + h5_names[j][2] + "_" + h5_names[j][3]
   f = h5py.File(filename, 'r')
   atl08_photon_data = pd.DataFrame([], columns=["segment_id", "ph_index",
                                              "ph_height"])

   for beam in beam_numbers:
      classed_PC_indx = pd.DataFrame(f[beam + '/signal_photons/classed_pc_indx'][:])
      ph_segment_id = pd.DataFrame(f[beam + '/signal_photons/ph_segment_id'][:])
      photon_class = pd.DataFrame(f[beam + '/signal_photons/classed_pc_flag'][:]) ## 0: noise, 1: ground, 2:canopy, 3: TOC
      ph_h = pd.DataFrame(f[beam + '/signal_photons/ph_h'][:])
      d_flag = pd.DataFrame(f[beam + '/signal_photons/d_flag'][:]) ## 0:noise 1:signal
      
      photon_df = pd.concat([ph_segment_id, classed_PC_indx, ph_h, photon_class,  d_flag], axis=1)
      photon_df.columns = ["segment_id", "ph_index", "ph_height", "photon_class", "d_flag"]
      photon_df = photon_df[photon_df["d_flag"]==1].reset_index(drop=True)
      photon_df = photon_df[(photon_df["photon_class"] == 2) | (photon_df["photon_class"] == 3)].reset_index(drop=True)
      photon_df = photon_df.drop(columns=["photon_class", "d_flag"], axis=1)
      atl08_photon_data = atl08_photon_data.append(photon_df)
  
   ## Find common segments between ATL08 and ATL03 data
   common_seg_ids = np.intersect1d(atl08_photon_data["segment_id"], atl03_photon_data["segment_id"])
   atl03_common_seg = atl03_photon_data[atl03_photon_data["segment_id"].isin(common_seg_ids)].reset_index(drop=True)
   atl08_common_seg = atl08_photon_data[atl08_photon_data["segment_id"].isin(common_seg_ids)].reset_index(drop=True)

   ## Combine lat lon data from ATL03 product with photon height data from ATL08 product using common segment id and photon index values
   ref_ph_lat_lon_h = pd.DataFrame([], columns=["reference_ph_lat", "reference_ph_lon", "ph_height"])
   
   for seg_id in common_seg_ids:
      atl03_sub = atl03_common_seg[atl03_common_seg["segment_id"] == seg_id].reset_index(drop=True)
      atl08_sub = atl08_common_seg[atl08_common_seg["segment_id"] == seg_id].reset_index(drop=True)
      if len(np.intersect1d(atl03_sub["index_within_seg"], atl08_sub["ph_index"])) > 0:
         for i in np.intersect1d(atl03_sub["index_within_seg"], atl08_sub["ph_index"]):
            lat = atl03_sub[atl03_sub["index_within_seg"] == i]["reference_ph_lat"].reset_index(drop=True)
            lon = atl03_sub[atl03_sub["index_within_seg"] == i]["reference_ph_lon"].reset_index(drop=True)
            height = atl08_sub[atl08_sub["ph_index"] == i]["ph_height"].reset_index(drop=True)
            photon_info = pd.concat([lat, lon, height], axis=1)
            ref_ph_lat_lon_h = ref_ph_lat_lon_h.append(photon_info, ignore_index=True)

   output = output.append(ref_ph_lat_lon_h, ignore_index=True)

output.to_csv("Reference_photon_height.csv", header=True, index=False)
