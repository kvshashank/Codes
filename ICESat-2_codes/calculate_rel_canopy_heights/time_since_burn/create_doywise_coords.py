import pandas as pd

data = pd.read_csv("rel_canopy_heights_w_doy", sep=" ", header=None, names=["lat", "lon", "can_height", "doy"])
uniq_doys = data["doy"].unique()

for doy in uniq_doys:
   data_sub = data[data["doy"] == doy].reset_index(drop=True)
   data_sub.to_csv("coords_" + str(doy), columns=["lat", "lon", "doy"], sep=" ", header=False, index=False)
