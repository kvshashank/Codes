import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import glob

for filename in glob.glob("cleaned_r.stats_doy_*"):
    print("Working on %s" %filename)
    data = pd.read_csv(filename, sep=" ", header=None)
    ncols = data.shape[1]
    
    ## Find date of ICESat-2 data collection
    doy = filename.split("_")[3]
    year=2019
    doy.rjust(3 + len(doy), '0')
    date = datetime.strptime(str(year) + "-" + doy, "%Y-%j")#.strftime("%m-%d-%Y")
    month = int(datetime.strptime(str(year) + "-" + doy, "%Y-%j").strftime("%m"))
    
    ## Calculate max possible days 
    modis_start_date = datetime.strptime("11-01-2000","%m-%d-%Y")
    max_days = abs((date - modis_start_date).days)
    
    ## Create a new dataframe called diff and store the days since last burn 
    col_start = ncols - month
    diff = pd.DataFrame([], columns=["diff"], index=np.arange(0, len(data))) 
    
    for i in range(0, len(data)):
       row_sum = data.iloc[i,2:col_start].sum()
       if (row_sum == 0):
           diff["diff"][i] = max_days
           
       else:
           nonzero_index_list = np.nonzero(np.array(data.iloc[i,:col_start]))[0]
           most_recent_burn_index = nonzero_index_list[-1] 
           month_number = most_recent_burn_index - 1             ## subtract first 2 columns and add 1 to account for python indexing
           future_date = modis_start_date + relativedelta(months=month_number)
           burn_year = future_date.strftime("%Y")
           burn_doy = data.iloc[i,most_recent_burn_index]
           if burn_doy > 0:
             burn_doy = str(int(burn_doy))
             burn_doy.rjust(3 + len(burn_doy), '0')
             burn_date = datetime.strptime(str(burn_year) + "-" + burn_doy, "%Y-%j")
             diff["diff"][i] = abs((date - burn_date).days)
    
    diff["diff"] = diff["diff"].dropna()
    diff["diff"] = diff["diff"]/365
    output = pd.concat((data.iloc[:,0:2], diff), axis=1, ignore_index=False)
    output = output.dropna()
    output.to_csv("time_since_burn_map_inputs_doy_" + doy, sep=" ", header=False, index=False)    
