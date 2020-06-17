## This code uses a deep neural network to predict plant community types
## THe data set used in this code is present at /home/vk5/ngee_arctic on theseus

# Seed value
seed_value=0

import os
os.environ['PYTHONHASHSEED'] = str(seed_value)

# 3. Set the `numpy` pseudo-random generator at a fixed value
import numpy as np
np.random.seed(seed_value)

# 4. Set the `tensorflow` pseudo-random generator at a fixed value
import tensorflow as tf
tf.random.set_seed(seed_value)

import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing
from keras.optimizers import Adam
from keras.layers import Dropout
from keras.constraints import maxnorm
from keras.utils import np_utils
from keras.regularizers import l2,l1
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import scipy.signal as signal
from sklearn.metrics import classification_report, confusion_matrix

data = pd.read_csv("reflec_final.csv")
data = data.drop_duplicates()
print data.shape
X = data.iloc[:,3:]
Y = data["Veg_type"]

# Split data into train and test
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size=0.2, random_state=seed_value, shuffle=True, stratify=Y)
k_fold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed_value)
cv_scores=[]

def standardize(X,Y,scaler):
  # Standardize the X values
  X_scaled = scaler.transform(X)

  # Convert veg labels to numbers
  encoder = LabelEncoder()
  encoder.fit(Y)
  encoded_Y = encoder.transform(Y)
  
  # Combine encoding along with label into a dataframe
  labels = pd.Series(list(encoder.inverse_transform(encoded_Y)), name="labels")
  encoded = pd.Series(encoded_Y, name="code")
  combined = pd.concat([encoded,labels], axis=1)
  label_code = combined.drop_duplicates().sort_values(ascending=True, by="code")

  # Convert number labels to one-hot encoding
  dummy_y = np_utils.to_categorical(encoded_Y)
  return(X_scaled,dummy_y, label_code)


def Model():
   model = Sequential()
   model.add(Dropout(0.1, input_shape=(378,)))
   model.add(Dense(200, activity_regularizer=l1(0.0005), input_dim=378, activation='relu'))
   model.add(Dropout(0.1))
   model.add(Dense(100, activity_regularizer=l1(0.0005), input_dim=200, activation='relu'))
   model.add(Dropout(0.1))
   model.add(Dense(50, activity_regularizer=l1(0.0005), input_dim=100, activation='relu'))
   model.add(Dropout(0.1))
   model.add(Dense(12, activation='softmax'))
   adam = Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=True)
   model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['acc'])
   return model

# Function to smooth the training and validation accuracy progression for plot
def smooth_data(history):
   N=3
   Wn=0.1
   B, A = signal.butter(N,Wn, output='ba')
   smooth_data_acc = signal.filtfilt(B,A, history.history['acc'])
   smooth_data_val_acc = signal.filtfilt(B,A, history.history['val_acc'])
   return (smooth_data_acc, smooth_data_val_acc)

def onehot_to_label(Y_Pred_onehot, label_code):
   y_pred_new = []
   for i in range(0, Y_Pred_onehot.shape[0]):
       index = np.argmax(Y_Pred_onehot[i,:])
       y_pred_new.append(label_code.iloc[index,1])
   return (y_pred_new)

i=0
plt.figure(figsize=(7.5,7.5))

for train, valid in k_fold.split(X_Train,Y_Train): 
   
   ## prepare train data
   scaler = preprocessing.StandardScaler().fit(X_Train.iloc[train])
   x_train,y_train,label_code = standardize(X_Train.iloc[train],Y_Train.iloc[train],scaler)
   x_valid,y_valid,label_code = standardize(X_Train.iloc[valid],Y_Train.iloc[valid],scaler)

   ## Train and Validate
   model = Model()
   history = model.fit(x_train, y_train, validation_data = (x_valid,y_valid), epochs=1650, verbose=0)

   ## Plot train and validation accuracy v/s epochs
   smooth_data_acc, smooth_data_val_acc = smooth_data(history)
   plt.plot(smooth_data_acc, linestyle='-', color="#8e7cc3ff")
   plt.plot(smooth_data_val_acc, linestyle='-', color="#f1c232ff")
   
   ## Print validation accuracy at the end of all epochs
   scores = model.evaluate(x_valid,y_valid, verbose=0)
   print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))
   cv_scores.append(scores[1]*100)
   i=i+1

print("%.2f%% (+/- %.2f%%)" %(np.mean(cv_scores), np.std(cv_scores)))

## Plot improvement in training and validation accuracies over epochs 
custom_lines=[]
custom_lines.append(Line2D([0],[0],color="#8e7cc3ff",linestyle='-', linewidth=3))
custom_lines.append(Line2D([0],[0],color="#f1c232ff",linestyle='-', linewidth=3))
plt.legend(custom_lines, ["Training","Validation"], fontsize=25)
plt.xlabel("Epochs", fontsize=20, labelpad=10, weight="bold")
plt.ylabel("Overall Accuracy (%)", fontsize=20, labelpad=10, weight="bold")
plt.yticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9], [0,10,20,30,40,50,60,70,80,90], fontsize=18)
plt.xticks(np.arange(0,1750,250), np.arange(0,1750,250), fontsize=18)
plt.title("8-fold cross validation", fontsize=20, weight="bold")
plt.savefig('plot.png')

# Test Set evaluation
scaler = preprocessing.StandardScaler().fit(X_Train)
x_test,y_test,label_code = standardize(X_Test,Y_Test,scaler)
score = model.evaluate(x_test,y_test, verbose=0)
print("Test set %s: %.2f%%" %(model.metrics_names[1], score[1]*100))

# Confusion Matrix and Precision/Recall stats
Y_Pred_onehot = model.predict(x_test, verbose=0)
y_pred = onehot_to_label(Y_Pred_onehot, label_code)
print (confusion_matrix(Y_Test, y_pred))
print(classification_report(Y_Test,y_pred))
print label_code
