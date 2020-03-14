"""
1. Load *.npy files into memory
2. For every .npy file, do:
   a. delete record if contain more than 8 Nan
   b. file prefix is the label
   c. create label array according to remaining records
3. Merge all .npy into 1 array
4. Merge all label array into 1 array
5. Run SVM
6. Save model into SVM-Hand.pkl

NOTE: Training has been disabled. Do not re-run this program.
Trained model has been saved as 'SVM-Hand.pkl'
"""

# Step 1: Import only the required package
import numpy as np
import os
import cv2
from sklearn.svm import SVC
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from matplotlib import pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

cPath = 'C:\\Hand-CA\\npy-train\\'
cModel = 'SVM-Hand.pkl'

arr = os.listdir(cPath)
train = []
tlabel = []
for pFile in arr:
    if pFile[-4:] != '.npy':
        continue
    label = pFile[0]
    print(pFile, 'Label:', label)
    data = np.load(cPath + pFile)

    for rec in data:
        zero = (data[0] == 0).sum()
        if zero < 8:
            train.append(rec)
            tlabel.append(label)

train = np.array(train)
tlabel = np.array(tlabel)

#check that the matrix shape is correct
print(data.shape, train.shape, tlabel.shape)

#model = SVC(kernel='linear')
#model.fit(train, tlabel)
#joblib.dump(model,cModel)      #save SVM model into file

