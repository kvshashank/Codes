#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd
import numpy as np
import pandas as pd
data = gpd.read_file('Q3_VegCompPlots_Seward.shp')
print data.head()


# In[2]:


# Create lookup table 
uniq_veg = data["vegtypeL3"].unique().tolist()
lookup_table = pd.DataFrame([],columns=["Code","Name"], index=np.arange(0,len(uniq_veg),1))
for i in range(0,len(lookup_table)):
    veg = uniq_veg[i]
    lookup_table["Name"][i] = veg
    uid = data[data["vegtypeL3"] == veg]["uid"].reset_index(drop=True)[0]
    lookup_table["Code"][i] = uid.split("-")[3]
print lookup_table


# In[3]:


bob = pd.read_csv("NGEEArctic_SewardPeninsula_Q3SamplingLocations_20191006_abreen - #2_Q3 Sampling points dGPS.csv", header=0)
bob = bob.iloc[0:164,:]
tf = bob["unique ID"].str.contains("VG-").dropna()
indices = tf[tf==True].index
bob = bob.iloc[indices,:]
bob = bob.reset_index(drop=True)
bob["unique ID"] = bob["unique ID"].replace("VG-COMP-","",regex=True)
bob["unique ID"] = bob["unique ID"].replace("_VG-COMP-","",regex=True)
bob["unique ID"] = bob["unique ID"].replace("VG-BIO-","",regex=True)
bob["unique ID"] = bob["unique ID"].replace("_","-",regex=True)


# In[4]:


print bob


# In[84]:


output = pd.DataFrame([],columns=["Site","Veg","Northing","Easting"],index=np.arange(0,len(bob)*4))
site_dict = {"CL":"Council","KG":"Kougarok","TL":"Teller"}
direction = ["NE","NW","SE","SW"]
j = 0

for direc in direction:
  nor_col = direc + "_Plot_Corner_UTM_Northing"
  eas_col = direc + "_Plot_Corner_UTM_Easting"
  for i in range (0, len(bob)):
    site = bob["unique ID"][i].split("-")[0]
    veg = bob["unique ID"][i].split("-")[1]
    lis = lookup_table[lookup_table["Code"] == veg]["Name"].tolist()
    if len(lis) > 0:
      output["Site"][j] = site_dict[site]
      output["Veg"][j] = lis[0]
      output["Northing"][j] = bob[nor_col][i] 
      output["Easting"][j] = bob[eas_col][i]
      j+=1  
output.to_csv("additional_points.csv")


# In[83]:


output.shape


# In[ ]:




