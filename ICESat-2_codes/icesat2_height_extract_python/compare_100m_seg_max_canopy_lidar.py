import os, h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import glob
import pyproj
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

shortlisted_seg = pd.read_csv("ATL08_shortlisted_segments.csv", header=0)
shortlisted_seg = shortlisted_seg[shortlisted_seg["night_flag"] == 1].reset_index(drop=True)

os.chdir("/home/vk5/icesat_2/ATL03_data/")

output = pd.DataFrame([], columns=["lats", "lons", "beam", "seg_id", "date", "uniq_id"])

for line in range(0, 500): #len(shortlisted_seg)):
   print("working on line %d in the shortlist file" %line)
   date_obj = datetime.strptime(shortlisted_seg["date"][line], '%d %B,%Y')
   date_str = datetime.strftime(date_obj, '%Y%m%d')
   file_pattern = "ATL03_" + date_str
   filename = glob.glob(file_pattern + "*.h5")
    
   ## If there is an ATL03 file present...
   if len(filename) > 0:

      ## Create a list of all the 20m segments
      seg_ids_20m = []
      for seg_id in range(shortlisted_seg["seg_id_begin"][line], (shortlisted_seg["seg_id_end"][line] + 1)):      
            seg_ids_20m.append(seg_id)
      
      ## Create a df with all the necessary ATL03 information    
      f = h5py.File(filename[0], 'r')
      beams = [1,2,3]  

      ### IMPORTANT: "Segment id" will be the same for all the three beams but the photon indices within each segment (Photon_id_count) would be different across the beams 
      for beam in beams:
        beam_num = '/gt' + str(beam) + 'r'
        ph_lats = pd.DataFrame(f[beam_num + "/heights/lat_ph"][:])
        ph_lons = pd.DataFrame(f[beam_num + "/heights/lon_ph"][:])
        ## Add a column with beam numbers
        beam_list = []
        for index in range(0, len(ph_lats)):
            beam_list.append(beam)
        beam_df = pd.DataFrame(beam_list, columns=[""])

        ## Create a df by concating all the above  
        photon_df = pd.concat([ph_lats, ph_lons, beam_df], axis=1, ignore_index=True)  
        photon_df.columns = ["lats", "lons", "beam"]        

        ## Create a df with segment information
        seg_id = pd.DataFrame(f[beam_num + "/geolocation/segment_id"][:])
        ph_start_index = pd.DataFrame(f[beam_num + "/geolocation/ph_index_beg"][:]) 
        seg_df = pd.concat([seg_id, ph_start_index], axis=1, ignore_index=True)
        seg_df.columns = ["seg_id", "ph_start_index"]
        
        ## Retain only shortlisted 20m seg ids
        seg_df = seg_df[seg_df["seg_id"].isin(seg_ids_20m)].reset_index(drop=True)
        
        ## For each seg_id extract lat lons of photons
        for index in range(0, (len(seg_df)-1)):
            photon_id_start = seg_df["ph_start_index"][index]
            photon_id_end = seg_df["ph_start_index"][index + 1] 
            photon_df_sub = photon_df.iloc[photon_id_start:photon_id_end,:]
            photon_df_sub = photon_df_sub.reset_index(drop=True)

            ## Create column of dates and segments
            dates=[]
            segment = []
            for i in range(0, len(photon_df_sub)):
                dates.append(date_str)
                segment.append(seg_df["seg_id"][index])
            dates = pd.DataFrame(dates, columns=[""])
            segment = pd.DataFrame(segment, columns=[""])

            ## Create a unique id
            uniqid = []
            for i in range(0, len(photon_df_sub)):
                uniqid.append(str(photon_df_sub["beam"][i]) + str(segment[""][i]) + str(dates[""][i]))
            uniqid = pd.DataFrame(uniqid, columns=[""])
 
            ph_data = pd.concat([photon_df_sub, segment, dates, uniqid], axis=1, ignore_index=True)           
            ph_data.columns = output.columns            

            ## Append photon_df_sub to the final output file
            output = output.append(ph_data, ignore_index=True)

## Convert lat lon to UTM
proj_wgs84 = pyproj.Proj(init='epsg:4326')
proj_utm = pyproj.Proj(init='epsg:32620')

utmx = pd.DataFrame([], index=np.arange(0, len(output)), columns=["Northing"])
utmy = pd.DataFrame([], index=np.arange(0, len(output)), columns=["Easting"])

x, y = pyproj.transform(proj_wgs84, proj_utm, output["lons"], output["lats"])
utmx["Northing"] = x
utmy["Easting"] = y

df = pd.concat([output, utmx, utmy], axis=1, ignore_index=True)
df = df.dropna()

df.columns = ["lats", "lons", "beam", "seg_id", "date", "uniq_id", "Northing", "Easting"]
df.to_csv("segment_wise_northing_easting.csv", sep=",", header=True, index=False, 
          columns=["Northing", "Easting", "uniq_id"])
