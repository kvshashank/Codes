import h5py
import pandas as pd
import numpy as np
import os, glob

os.chdir("/home/vk5/postdoc/calculate_rel_canopy_heights")

for file_name in sorted(glob.glob("ATL03_*_stats.csv")):
    print("working on %s" %(file_name))
    file_pattern = file_name.split("_")[2]
    beam_num = file_name.split("_")[5]
    
    ##### Drop unwanted columns from ATL03 stats files
    stats_file = pd.read_csv(file_name, header=0, sep=",")
    data_slice = pd.concat([stats_file["seg_start_lat_interp (deg)"], stats_file["seg_end_lat_interp (deg)"],
                        stats_file["seg_start_lon_interp (deg)"], stats_file["seg_end_lon_interp (deg)"],
                        stats_file["seg_start_delta_time_interp (sec)"], stats_file["seg_end_delta_time_interp (sec)"], stats_file["atl03_all_canopy_relative_height (m HAE)"]],
                        axis=1)
    data_slice["lat"] = (data_slice["seg_start_lat_interp (deg)"] + data_slice["seg_end_lat_interp (deg)"])/2
    data_slice["lon"] = (data_slice["seg_start_lon_interp (deg)"] + data_slice["seg_end_lon_interp (deg)"])/2
    data_slice = data_slice.drop(columns=["seg_start_lat_interp (deg)", "seg_end_lat_interp (deg)", "seg_start_lon_interp (deg)", "seg_end_lon_interp (deg)"])
    data_slice_rearr = pd.concat([data_slice["lat"], data_slice["lon"], data_slice["seg_start_delta_time_interp (sec)"], data_slice["seg_end_delta_time_interp (sec)"], data_slice["atl03_all_canopy_relative_height (m HAE)"]], 
                                 axis=1)
    data_slice_rearr.columns = ["lat", "lon", "seg_start_dt", "seg_end_dt", "rel_canopy_heights"]
    data_slice_rearr = data_slice_rearr.dropna().reset_index(drop=True)

    #### Extract data quality info from ATL08 hdf5 files
    os.chdir("/home/vk5/postdoc/ATL08_h13v10")
    f = h5py.File(glob.glob("ATL08_*" + file_pattern + "*.h5")[0], 'r')
    dt_begin= pd.DataFrame(f[beam_num + "/land_segments/delta_time_beg"][:], columns=[""])
    dt_end = pd.DataFrame(f[beam_num + "/land_segments/delta_time_end"][:], columns=[""])
    water_mask = pd.DataFrame(f[beam_num + "/land_segments/segment_watermask"][:], columns=[""]) ## 0 is no water, 1 is water. Derived from 250m water mask. 
    canopy_rh_conf = pd.DataFrame(f[beam_num + "/land_segments/canopy/canopy_rh_conf"][:], columns=[""]) ## 2 is good
    cloud_flag_atm = pd.DataFrame(f[beam_num + "/land_segments/cloud_flag_atm"][:], columns=[""]) ## 0 is good
    
    flag_data = pd.concat([dt_begin, dt_end, water_mask, canopy_rh_conf, cloud_flag_atm], axis=1)
    flag_data.columns=["dt_begin", "dt_end", "water_mask", "canopy_rh_conf", "cloud_flag_atm"]
    
    ## Remove unwanted segments
    flag_data_clean = flag_data[(flag_data["water_mask"] == 0) & (flag_data["canopy_rh_conf"] == 2) 
                            & (flag_data["cloud_flag_atm"] == 0)].reset_index(drop=True)
    
    ##### Remove 30m segments from ATL03 stats files that don't pass the minimum data quality standards
    ### The delta time corresponding to both the start and end of each 30m segment should satisfy the data quality requirements 
    stats_clean = pd.DataFrame([], columns=data_slice_rearr.columns)
    
    for i in range(0, len(data_slice_rearr)):
        dt_30mseg_start = data_slice_rearr["seg_start_dt"][i]
        dt_30mseg_end = data_slice_rearr["seg_end_dt"][i]

        if((len(flag_data_clean[flag_data_clean["dt_begin"] <= dt_30mseg_start]) > 0) & len(flag_data_clean[flag_data_clean["dt_begin"] <= dt_30mseg_end]) > 0):
           index_start = flag_data_clean[flag_data_clean["dt_begin"] <= dt_30mseg_start].index[-1]
           index_end = flag_data_clean[flag_data_clean["dt_begin"] <= dt_30mseg_end].index[-1]        

           if((flag_data_clean["dt_end"][index_start] >= dt_30mseg_start) & (flag_data_clean["dt_end"][index_end] >= dt_30mseg_end)):
              stats_clean = stats_clean.append(data_slice_rearr.iloc[i,:], ignore_index=True)
    
    output_filename = file_name.split("s")[0] + "clean_stats.csv"
    os.chdir("/home/vk5/postdoc/calculate_rel_canopy_heights")
    stats_clean.to_csv(output_filename, columns=["lat", "lon", "rel_canopy_heights"], header=False, index=False)
