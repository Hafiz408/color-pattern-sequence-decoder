import cv2
import os
from datetime import datetime


path = "D:\subhikshaa\project\Codeathon-2023\Result1"
os.chdir(path)

i = 0
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FPS,30)

while True:
    ret, img = video.read()
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(img, str(datetime.now()), (20, 40),
                font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("live video", img)
    
    key = cv2.waitKey(25)
    if key == ord("q"):
        break

    filename = "Frame_" + str(i) + ".jpg"
    cv2.imwrite(filename, img)
    i += 1

# close the camera
video.release()

# close open windows
cv2.destroyAllWindows()