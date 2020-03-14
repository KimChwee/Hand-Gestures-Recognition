"""
Once feature extraction program for 1 video is done
This program is used to call the program looping thru all videos in specified folder
Recommend to run this program via command prompt to be able to see error message if any

Video processing take a long time so initially, this is done 1 by 1. There are more than
50 videos in total. Due to the long processnig time, as and when 1 video is done,
it is added to SVM model for training and validation while the next video is being run

Take note not to put all videos in the folder until fully tested and able to leave it to
run while sleeping
"""
import numpy as np
import os

cPath = 'C:\\Hand-CA\\dataset\\'

arr = os.listdir(cPath)
for pFile in arr:
    if pFile[-4:] != '.mp4':
        continue
    label = pFile[0]
    #print(pFile, 'Label:', label)
    os.system('python handVidFull.py ' + pFile[:-4])



