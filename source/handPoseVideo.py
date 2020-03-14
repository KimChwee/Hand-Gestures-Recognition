"""
    ISS KE30 Aug-2019
    Initial coding during research phase to see if this can be appropriate
    for CA topics

    The aim is to read video and extract hand joint coordinates,
    output the result into another video to validate how good is the result

"""
import cv2
import time
import numpy as np
import csv

protoFile = "../hand/pose_deploy.prototxt"
weightsFile = "../hand/pose_iter_102000.caffemodel"   #need to download from source to always have the latest version. also too big to submit
nPoints = 22
POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

threshold = 0.2
fName = 'L-001'

cPath = 'C:\\Hand-CA\\'
#input_source = "asl.mp4"
input_source = cPath + 'dataset\\' + fName + '.mp4'
cap = cv2.VideoCapture(input_source)
hasFrame, frame = cap.read()

frameWidth = frame.shape[1]
frameHeight = frame.shape[0]

aspect_ratio = frameWidth/frameHeight

inHeight = 368
inWidth = int(((aspect_ratio*inHeight)*8)//8)

vid_writer = cv2.VideoWriter(fName + '.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame.shape[1],frame.shape[0]))

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
k = 0
result = []
while 1:
    k+=1

    t = time.time()
    hasFrame, frame = cap.read()
    frameCopy = np.copy(frame)
    if not hasFrame:
        #cv2.waitKey()
        break

    # speed up extraction first
    if k % 10 != 0:
        continue
    
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                              (0, 0, 0), swapRB=False, crop=False)

    net.setInput(inpBlob)

    output = net.forward()

    #print("forward = {}".format(time.time() - t))

    # Empty list to store the detected keypoints
    points = []
    for i in range(nPoints):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]
        probMap = cv2.resize(probMap, (frameWidth, frameHeight))

        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        if prob > threshold :
            cv2.circle(frameCopy, (int(point[0]), int(point[1])), 6, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frameCopy, "{}".format(i), (int(point[0]), int(point[1])), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2, lineType=cv2.LINE_AA)

            # Add the point to the list if the probability is greater than the threshold
            points.append((int(point[0]), int(point[1])))
        else :
            points.append(None)
    #breakpoint()
    # <Points> now contains all the 22 coordinates of the hand joint
            
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 1, lineType=cv2.LINE_AA)
            cv2.circle(frame, points[partA], 1, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(frame, points[partB], 1, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    #print("Time Taken for frame = {}".format(time.time() - t))

    # cv2.putText(frame, "time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (255, 50, 0), 2, lineType=cv2.LINE_AA)
    # cv2.putText(frame, "Hand Pose using OpenCV", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 50, 0), 2, lineType=cv2.LINE_AA)
    # Save the 22 points snapshot to result every 10 frame

    if k % 10 == 0:
        temp = []
        for i in range(nPoints):
            if points[i] == None:
                points[i] = (0,0)
            temp.extend(points[i])
        result.append(temp)
                
    cv2.imshow('Output-Skeleton', frame)
    # cv2.imwrite("video_output/{:03d}.jpg".format(k), frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

    #print("total = {}".format(time.time() - t))
    print(k)
    vid_writer.write(frame)

vid_writer.release()
cv2.destroyAllWindows()

result = np.array(result)
np.save(fName, result)   #file name will auto have .npy extension
#newArray = np.load('output.npy')
