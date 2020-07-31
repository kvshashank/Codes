## Data for this is present at /home/vk5/ngee_arctic/niche_modeling/area_occupied_by_each_plant_comm on theseus
## This code creates a table of area occupied by plant community

import pandas as pd
import numpy as np

council = pd.read_csv("council_plant_commwise_count", sep=" ", header=None, names=["plant_id","pixels"])
kougarok = pd.read_csv("kougarok_plant_commwise_count", sep=" ", header=None, names=["plant_id","pixels"])
teller = pd.read_csv("teller_plant_commwise_count", sep=" ", header=None, names=["plant_id","pixels"])

df = pd.concat([council, kougarok["pixels"], teller["pixels"]], axis=1)
df.columns = ["plant_id", "council_pixels", "kougarok_pixels", "teller_pixels"]
df_new = pd.DataFrame([], index=np.arange(0,len(df),1), columns=["plant_comm_names", "pixels_sum", "area (km^2)"])
df = pd.concat([df, df_new], axis=1)

plant_comm_names=["Dry Lic", "Eric Dwrf", "Sed-Wil", "Mes Gram", "Tuss Lich", "Mix Shrb", "Bir-Eric", "Wil Shrb", "Ald-Wil", "Wil Bir", "Wet Mead", "Wet Sed"]
for i in range(0, len(df)):
    df["plant_comm_names"][i] = plant_comm_names[i]
    df["pixels_sum"][i] = df["council_pixels"][i] + df["kougarok_pixels"][i] + df["teller_pixels"][i]
    df["area (km^2)"][i] = (df["pixels_sum"][i] * 25)/(1000*1000)

print(df.sort_values(by="area (km^2)", ascending=False))

