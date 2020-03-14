import cv2

cPath = 'C:\\Hand-CA\\'
source_video = 'dataset\\1-001.mp4'
vidcap = cv2.VideoCapture(cPath + source_video)
# Find OpenCV version
fps = vidcap.get(cv2.CAP_PROP_FPS)
fps = 8
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))

#fps = 20        # 20 FPS is good enough for most scenario. Adjust as required
fourcc = cv2.VideoWriter_fourcc('X','V','I','D') #you can use other codecs as well.
#vid = cv2.VideoWriter('record.avi', fourcc, fps, (width,height))

count = 0
success = True
while success:
    success,image = vidcap.read()
    #vid.write(image)
    cv2.imshow("frame", image)
    key = cv2.waitKey(1)
    if key == 27:   #Esc to close window
        break    

#vid.release()
vidcap.release()
cv2.destroyAllWindows()
