# THis code calcualtes mean and std dev for each row in the precip and temp r.stats files
# The data is present at the location /home/vk5/ngee_arctic/niche_modeling/generate_maps_bioclim_vars on theseus machine

import pandas as pd
import os
import numpy as np
import glob

os.chdir("/home/vk5/ngee_arctic/niche_modeling/generate_maps_bioclim_vars")
columns=["X","Y","mean","std_dev"]
for file_name in glob.glob("*"):
    data = pd.read_csv(file_name, sep=" ", header=None)
    new_file = pd.DataFrame([], index=np.arange(0,len(data),1), columns=columns)
    for i in range(0, len(new_file)):
        new_file["X"][i] = data.iloc[i,0]
        new_file["Y"][i] = data.iloc[i,1]
        new_file["mean"][i] = round(np.mean(data.iloc[i,2:]),2)
        new_file["std_dev"][i] = round(np.std(data.iloc[i,2:]),2)
    output=file_name + "_stats"
    new_file.to_csv(output, sep=" ", index=False, header=False)
