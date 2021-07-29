import pandas as pd
import numpy as np
import glob

for filename in sorted(glob.glob("r.stats_burn_*")):
    print("working on %s" %filename)
    doy = filename.split("_")[4]
    data = pd.read_csv(filename, sep=" ", header=None)
    data["sum"] = data.iloc[:,2:].sum(axis=1)
    data = data[data["sum"] >= 0].reset_index(drop=True)
    data["count"] = data.iloc[:,2:].count(axis=1)
    data = data[data["count"] > 100].reset_index(drop=True)
    data = data.drop(columns=["sum","count"], axis=1)
    output_filename = "cleaned_r.stats_doy_" + str(doy) 
    data.to_csv(output_filename, sep=" ", header=False, index=False)
