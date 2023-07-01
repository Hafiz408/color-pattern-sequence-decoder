import cv2
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
rootdir = 'ML'




# Function to find dominant color from frame from webcam
def find_dominant_color(frame):
    # Convert the frame from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Reshape the frame to a flattened array of pixels
    pixels = frame.reshape(-1, 3).astype(np.float32)

    # Define the criteria for K-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Perform K-means clustering
    _, _, centers = cv2.kmeans(pixels, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert the center values to the uint8 data type
    center_color = np.uint8(centers[0])
    r, g, b = center_color

    return r, g, b

red,blue,green,labels = [],[],[],[]
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(file)
        img = cv2.imread(os.path.join(subdir,file))
        r,g,b = find_dominant_color(img)
        label = subdir[3:]
        red.append(r)
        green.append(g)
        blue.append(b)
        labels.append(label)

df = pd.DataFrame()
df.insert(loc=0, column='R', value=red)
df.insert(loc=1, column='G', value=green)
df.insert(loc=2, column='B', value=blue)
df.insert(loc=3, column='Label', value=labels)
print(df.head())
df.to_csv("colors.csv")