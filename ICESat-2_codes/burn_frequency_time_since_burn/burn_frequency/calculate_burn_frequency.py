## Data for this code is present at /home/vk5/postdoc/MCD64

import pandas as pd
import numpy as np

data = pd.read_csv("modis_20yr_burn_dates_h13v10", sep=" ", header=None)
data["counter"] = data.astype(bool).sum(axis=1)
data["counter"] = data["counter"] - 2
data.to_csv("cumulative_burn_frequency_h13v10", sep=" ", header=False, index=False, columns=[0, 1, "counter"])
