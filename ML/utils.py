import cv2
import os
from datetime import datetime

path = "ML/Dataset/grey/"
os.mkdir(path)

i = 0
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FPS,30)

def crop_frame_center(img,width_scale=0.25,height_scale=0.25):
    center = img.shape
    h,w=center[0]*height_scale,center[1]*width_scale
    x = center[1]/2 - w/2
    y = center[0]/2 - h/2

    return img[int(y):int(y+h), int(x):int(x+w)]


wait=0
while True:
    ret, img = video.read()
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.imshow("live video", img)
    
    wait+50
    key = cv2.waitKey(250)
    if i==20:
        break

    if wait%1000==0:

        filename = "Frame_" + str(i) + ".jpg"
        img=crop_frame_center(img)
        cv2.imwrite(filename, img)
        i += 1

# close the camera
video.release()