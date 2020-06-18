## This code uses a Random Forest model to predict plant community types using topographic variables
## It uses plant community maps for the extended watersheds. The extent of these maps is based on the solar irradiation maps
## The data used in this code is available at /home/vk5/ngee_arctic/niche_modeling on theseus 

# Seed value
seed_value=0

import os
os.environ['PYTHONHASHSEED'] = str(seed_value)

# 3. Set the `numpy` pseudo-random generator at a fixed value
import numpy as np
np.random.seed(seed_value)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing, metrics
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

print("ingesting data")
data=pd.read_csv("combined_niche_model_inputs_7vars", sep=" ", header=None, names=["slope","sin_aspect","cos_aspect","elevation","topo_wetness_index","summer_solar_irr",
                 "winter_solar_irr","plant_comm"])

print("Considering only the following 6 plant communties: Alder-Willow Shrub, Dryas-Lichen Dwarf Shrub Tundra, Mixed shrub-sedge Tussock Tundra", "Tussock-Lichen Tundra", "Wet-Sedge Bog-Meadow", "Willow-Birch Shrub")
plant_comm = [21,25,26,29,30,37]
data = data[data["plant_comm"].isin(plant_comm)].reset_index(drop=True)

print("Dividing data into X and Y")

X = data.iloc[:,0:7]
Y = data.iloc[:,7]
print("begin training")
# Split data into train and test
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.2, random_state=seed_value, shuffle=True, stratify=Y)
k_fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed_value)
cv_scores=[]

def standardize(X,scaler):
  X_scaled = scaler.transform(X)
  return(X_scaled)

i=1
for train, valid in k_fold.split(X_Train,Y_Train):
    print("iteration number %d" %i) 
    # Scale the training and validation data
    scaler = preprocessing.StandardScaler().fit(X_Train.iloc[train])
    X_train_scaled = standardize(X_Train.iloc[train], scaler)
    X_valid_scaled = standardize(X_Train.iloc[valid], scaler)
    Y_train = Y_Train.iloc[train]
    Y_valid = Y_Train.iloc[valid]

    RF = RandomForestClassifier(n_estimators=100, random_state=seed_value, n_jobs=20, class_weight="balanced", min_samples_split=30)
    RF.fit(X_train_scaled,Y_train)
    Y_valid_pred = RF.predict(X_valid_scaled)
    acc = metrics.accuracy_score(Y_valid,Y_valid_pred)
    cv_scores.append(acc*100)
    i+=1

print("Validation: %.2f%% (+/- %.2f%%)" %(np.mean(cv_scores), np.std(cv_scores)))

# Test set evaluation
scaler = preprocessing.StandardScaler().fit(X_Train)
x_test = standardize(X_Test,scaler)
y_test_pred = RF.predict(x_test)
percent_acc = (metrics.accuracy_score(Y_Test,y_test_pred))*100

print("Test set accuracy: %.2f%%" %percent_acc)
