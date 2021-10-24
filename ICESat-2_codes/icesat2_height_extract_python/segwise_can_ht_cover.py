import pandas as pd
import glob, os
import numpy as np

os.chdir("/home/vk5/postdoc/calculate_recovery/photon_data_extraction")
for name in sorted(glob.glob("photon_data_*.csv")):
    os.chdir("/home/vk5/postdoc/calculate_recovery/photon_data_extraction")
    print("working on %s" %name)
    data = pd.read_csv(name, sep=" ", header=None, names=["lat", "lon", "id2", "ph_h", "photon_classify", "day_night", "month"])
    data["photon_classify"] = data["photon_classify"].replace(3,2)
    data_groupby = data.groupby(["id2"])["photon_classify"].value_counts()
    id2 = pd.DataFrame(data_groupby.index.get_level_values(0), columns=["id2"])
    photon_classify = pd.DataFrame(data_groupby.index.get_level_values(1), columns=["photon_classify"])
    counts = pd.DataFrame(data_groupby.tolist(), columns=["counts"], index=np.arange(0, len(id2)))
    df = pd.concat([id2, photon_classify, counts], axis=1)
    
    ### Apply groupby again to select only those segs which have ground photons (1,2)
    ground_groupby = df.groupby(["id2"])["photon_classify"].sum() 
    id2_sub = pd.DataFrame(ground_groupby.index.get_level_values(0), columns=["id2"])
    sums = pd.DataFrame(ground_groupby.tolist(), columns=["sums"], index=np.arange(0, len(id2_sub)))
    df_sub = pd.concat([id2_sub, sums], axis=1)
    ok_sums = [3]
    df_sub = df_sub[df_sub["sums"].isin(ok_sums)].reset_index(drop=True)

    ### Go back to the original file and extract only valid segs
    data = data[data["id2"].isin(df_sub["id2"])].reset_index(drop=True)

    ### Calculate std dev of ground heights
    ground_data = data[data["photon_classify"] == 1].reset_index(drop=True)
    ground_ht_std = pd.DataFrame(ground_data.groupby(["id2"])["ph_h"].std().tolist(), columns=["ground_ht_std"])
    ids = pd.DataFrame(ground_data.groupby(["id2"])["ph_h"].std().index.get_level_values(0), columns=["id2"])    
    ground_heights_std_df = pd.concat([ids, ground_ht_std], axis=1) 
  
    ### Calculate n_ground photons and canopy cover
    photon_count_groupby  = data.groupby(["id2","photon_classify"]).count()
    id2_sub = pd.DataFrame(photon_count_groupby.index.get_level_values(0), columns=["id2"])
    photon_classify =  pd.DataFrame(photon_count_groupby.index.get_level_values(1), columns=["photon_classify"])
    ph_counts = pd.DataFrame(photon_count_groupby["ph_h"].tolist(), columns=["counts"], index=np.arange(0, len(id2_sub)))
    ph_count_df = pd.concat([id2_sub, photon_classify, ph_counts], axis=1)
    n_ground_ph = ph_count_df[ph_count_df["photon_classify"] == 1].reset_index(drop=True)
    n_ground_ph = n_ground_ph.drop(["photon_classify"], axis=1)
    n_ground_ph.columns = ["id2", "n_ground_ph"]
    n_canopy_ph = ph_count_df[ph_count_df["photon_classify"] == 2].reset_index(drop=True)
    n_canopy_ph = n_canopy_ph.drop(["photon_classify"], axis=1)
    n_canopy_ph.columns = ["id2", "n_canopy_ph"]
    n_gr_cnp_ph_df = n_ground_ph.merge(n_canopy_ph, how="inner", on="id2")
    n_gr_cnp_ph_df["sum_photons"] = n_gr_cnp_ph_df["n_ground_ph"] + n_gr_cnp_ph_df["n_canopy_ph"]
    n_gr_cnp_ph_df["canopy_cover"] = (n_gr_cnp_ph_df["n_canopy_ph"]/n_gr_cnp_ph_df["sum_photons"])*100
    n_gr_cnp_ph_df = n_gr_cnp_ph_df.drop(["sum_photons"], axis=1)
    n_gr_cnp_ph_df["canopy_cover"] = n_gr_cnp_ph_df["canopy_cover"].round(decimals=2)
    
    ### Calculate rel canopy height for each 20m segment
    can_height_groupby = data.groupby(["id2","photon_classify"])["ph_h"].mean()
    id2_sub = pd.DataFrame(can_height_groupby.index.get_level_values(0), columns=["id2"])
    photon_classify =  pd.DataFrame(can_height_groupby.index.get_level_values(1), columns=["photon_classify"]) 
    ph_h_avg = pd.DataFrame(can_height_groupby.tolist(), columns=["avg_can_height"], index=np.arange(0, len(id2_sub)))
    can_height_df = pd.concat([id2_sub, photon_classify, ph_h_avg], axis=1)
    can_height_df = can_height_df[can_height_df["photon_classify"] == 2].reset_index(drop=True)
    can_height_df = can_height_df.drop(["photon_classify"], axis=1)
    
    ### Merge all dataframes
    can_height_df = can_height_df.merge(n_gr_cnp_ph_df, how="inner", on="id2")
    data_sub = data.drop_duplicates(subset=["id2"]).reset_index(drop=True)
    data_sub = data_sub.drop(["photon_classify", "ph_h"], axis=1)
    output = data_sub.merge(can_height_df, how="inner", on="id2")
    output = output.merge(ground_heights_std_df, how="inner", on="id2")
    file_code_1 = name.split("_")[2][2:9]
    file_code_2 = name.split("_")[3][2]
    file_code = file_code_1 + file_code_2 
    output["id1"] = file_code
    output = pd.concat([output["lat"], output["lon"], output["id1"], output["id2"], output["n_ground_ph"], output["ground_ht_std"], output["n_canopy_ph"], output["canopy_cover"], output["avg_can_height"],
                        output["day_night"], output["month"]], axis=1)
    output = output.dropna()
    os.chdir("/home/vk5/postdoc/calculate_recovery/segwise_canopy_cover_grd_photons")
    output_name = name.split(".")[0] + "_info_extract"
    output.to_csv(output_name, sep=" ", header=False, index=False) 
