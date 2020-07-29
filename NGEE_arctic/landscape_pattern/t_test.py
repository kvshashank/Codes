## This code calculates p-values for the difference in proportion of each plant community downstream of alder vs anywhere else on the watershed
## Data for this available at /home/vk5/ngee_arctic/alder_upstream_downstream

import pandas as pd

data = pd.read_csv("kougarok_upstream_percent_and_area_alder", sep=" ", header=0)

uniq_plant_comm = sorted(data["plant_comm"].unique())
thresh=20

print("Total sample size = %d" %len(data[data["percent_alder"]>thresh]))

for plant_comm in uniq_plant_comm:
   data_sub = data[(data["plant_comm"]==plant_comm) & (data["percent_alder"] > thresh)].reset_index(drop=True)
   print("%d, %d" %(plant_comm, len(data_sub)))
