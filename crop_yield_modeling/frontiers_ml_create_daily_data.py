#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
os.chdir('C:/Users/sds lab/Desktop/class/Machine Learning/project/Data')
raw_data=pd.read_csv('Cerro_Gordo_weather_data.csv',sep=',',header=0)

# Convert strings to datetime
for row in range(0, raw_data.shape[0]):
    raw_data.iloc[row,1] = datetime.strptime(raw_data.iloc[row,1],'%Y-%m-%d')


# In[ ]:


raw_data_sorted = raw_data.sort_values(by='DATE',axis=0,ascending=True)
meaningful_data = pd.DataFrame()
# Remove dates outside Growing season
years=list(range(1940,2018))
for year in years:
    start_date = datetime.strptime(str(year) + '-05-10', '%Y-%m-%d')
    end_date = datetime.strptime(str(year) + '-10-20', '%Y-%m-%d')
    meaningful_data = meaningful_data.append(raw_data_sorted[(raw_data_sorted.iloc[:,1]>=start_date) & (raw_data_sorted.iloc[:,1]<=end_date)], ignore_index=True)


# In[ ]:


unique_dates = np.sort(meaningful_data.iloc[:,1].unique())
precip=[]
tmax=[]
tmin=[]
for i in range(0, len(unique_dates)):
    daily_subset = meaningful_data[meaningful_data.iloc[:,1]==unique_dates[i]]
    precip.append(daily_subset.iloc[:,2].mean())
    tmax.append(daily_subset.iloc[:,3].mean())
    tmin.append(daily_subset.iloc[:,4].mean())


# In[ ]:


daily_weather = pd.concat([pd.DataFrame(unique_dates), pd.DataFrame(precip), pd.DataFrame(tmax), pd.DataFrame(tmin)], axis=1,ignore_index=True)
import matplotlib.pyplot as plt
#os.chdir('C:/Users/sds lab/Desktop/class/Machine Learning/project/Data')

#daily_weather.to_csv('Cerro_Gordo_daily_weather.csv', sep=',')

fig, ax1 = plt.subplots(figsize=(10,5))
Tmax, = ax1.plot(daily_weather.iloc[:,0],daily_weather.iloc[:,2],'ro' ,alpha=0.1, label='Daily Max Temp')
Tmin, = ax1.plot(daily_weather.iloc[:,0],daily_weather.iloc[:,3], 'bo',alpha=0.1, label='Daily Min Temp')
ax2 = ax1.twinx()
Pcp, = ax2.plot(daily_weather.iloc[:,0], daily_weather.iloc[:,1], 'go', alpha=0.1, label='Daily Precip')

ax1.set_xlabel('Year')
ax1.set_ylabel('Daily Min/Max Temp (C)', fontsize=12)
ax1.set_title('Time series of daily weather for county', fontsize=14)
ax1.xaxis.set_tick_params(labelsize=12)
ax1.yaxis.set_tick_params(labelsize=12)
ax2.yaxis.set_tick_params(labelsize=12)
ax2.set_ylabel('Daily Precip (mm)', fontsize=12)
plt.legend(handles=[Tmax, Tmin, Pcp])
plt.show()


# In[ ]:


import os

os.chdir('C:/Users/sds lab/Desktop/class/Machine Learning/project/Data')

fig, ax = plt.subplots(figsize=(10,5))
corn_yield = pd.read_csv('Cerro_Gordo_crop_yields.csv',sep=',',header=0)
plt.plot(corn_yield.iloc[:,0], corn_yield.iloc[:,1], '-bo')
plt.ylabel('Corn Yield (bu/acre)', fontsize=12)
plt.xlabel('Year', fontsize=12)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)
plt.title('Time Series of Corn Yields for the county', fontsize=14)
plt.show()

