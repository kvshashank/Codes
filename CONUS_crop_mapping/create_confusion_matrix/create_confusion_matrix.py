## Data for this is available at /home/vk5/create_confusion_matrix of theseus
## This creates a confusion matrix from the r.stats files

import numpy as np

data = np.loadtxt('r.stats_sub2_24', dtype=int)
conf_mat = np.zeros(shape=(8,8))
crops=[1,5,24,61,37,36,4,3]
for i in range(0,len(crops)):
  for j in range(0,len(crops)):
     crop_pix = data[(data[:,0]==crops[i]) & (data[:,1]==crops[j]) ,2] 
     crop_pix_hect = (crop_pix*0.099)/1000  # in thousands of hectares
     conf_mat[i,j] = crop_pix_hect

np.savetxt("confusion_matrix_24", conf_mat, fmt='%d')
