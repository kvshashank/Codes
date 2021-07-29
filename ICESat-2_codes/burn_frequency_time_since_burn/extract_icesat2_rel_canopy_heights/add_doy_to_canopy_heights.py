import pandas as pd
import numpy as np
import glob
from datetime import datetime

output = pd.DataFrame([],columns=["lat","lon","rel_height", "doy"])

for file_name in sorted(glob.glob("*_clean_stats.csv")):
    date_str = file_name.split("_")[1][0:8]
    date = datetime.strptime(date_str, "%Y%m%d")
    doy = int(date.strftime("%j"))
    data = pd.read_csv(file_name, header=None)
    data["doy"] = doy
    data.columns = output.columns
    output = output.append(data, ignore_index=True)

output.to_csv("rel_canopy_heights_w_doy", sep=" ", header=False, index=False)
