# importing required libraries
import cv2
import numpy as np
import time
from env import *
import collections

# map color pixel values to valid pixel values
def closest_value(input_value):
  arr = np.array([0, 128, 192, 255])
  i = (np.abs(arr - input_value)).argmin()
  return arr[i]

def skip_frames(fps,duration):
    return round(duration/(1000/fps))

SKIP_FR = skip_frames(FPS,MIN_COLOR_DURATION)

def closest_rgb(r,g,b):
   r = closest_value(r)
   g = closest_value(g)
   b = closest_value(b)

   return (r,g,b)

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

# Find partial patterns
def partialMatch(subset):
    for i in range(len(keys)):
        j=0
        while(j<len(subset)):
            if subset[j]!=keys[i][j]:
                break
            j+=1
        if j==len(subset):
            print("Partial Pattern ",i+1)
            return

# find the valid pattern for the given 4 color sequence
def decode_sequence(seq):
   return valid_pattern.get(tuple(seq), 'Invalid')

def capture_color_sequence(**kwargs):
    
    left,right=0,0
    q=collections.deque()

    color_seq = collections.deque()

    if 'video_file' in kwargs:
        # taking input from video file
        vid = cv2.VideoCapture(kwargs['video_file'])
    else:
        # taking the input from webcam
        vid = cv2.VideoCapture(0)

    milliseconds = 0
    wait = 0
    while vid.isOpened():
        
        # capturing the current frame
        valid, frame = vid.read()
        
        if 'video_file' not in kwargs and wait % SKIP_FR != 0:
            wait+=1
            continue
        wait+=1
        if not valid:
            if right==4:
                tup=tuple(color_seq)
                if tup in keys:
                    if len(q)>1 and len(q)<=3:
                        partialMatch(tuple(q))
                    q.clear()
                    print("Valid Pattern ",valid_pattern[tup])
                    color_seq.clear()
                else:
                    if len(q)>1 and len(q)<=3:
                        partialMatch(tuple(q))
                        temp=len(q)
                        q.clear()
                    else:
                        print("Invalid Pattern")
                        temp=1
                    q.append(color_seq[0])
                    while temp:
                        color_seq.popleft()
                        temp-=1
            right=right+1
            break

        # displaying the current frame
        cv2.imshow("frame", frame)

        if 'video_file' not in kwargs:
            # find dominant color from frame
            r_estimate, g_estimate, b_estimate = find_dominant_color(frame)
        else:
            # setting values for base colors
            b = frame[:, :, :1]
            g = frame[:, :, 1:2]
            r = frame[:, :, 2:]

            # computing the mean
            b_estimate = np.mean(b)
            g_estimate = np.mean(g)
            r_estimate = np.mean(r)

        # finding closest rgb from estimate
        rgb = closest_rgb(r_estimate, g_estimate, b_estimate)
        color = dec_to_color.get(rgb, '404')

        # print((r_estimate,g_estimate,b_estimate), rgb, color)

        #color_seq.append(color)

        # avoid invalid colors
        if right==4:
                tup=tuple(color_seq)
                if tup in keys:
                    if len(q)>1 and len(q)<=3:
                        partialMatch(tuple(q))
                    q.clear()
                    print("Valid Pattern ",valid_pattern[tup])
                    color_seq.clear()
                    right=0
                else:
                    if len(q)>1 and len(q)<=3:
                        partialMatch(tuple(q))
                        temp=len(q)
                        q.clear()
                    else:
                        print("Invalid Pattern")
                        temp=1
                    q.append(color_seq[0])
                    while temp:
                        color_seq.popleft()
                        right-=1
                        temp-=1

        #print(left,right,color)
        if color != '404':
            if right>2 and (color_seq[right-1]==color  and color_seq[right-2]==color):
                continue
            color_seq.append(color)
            right=right+1

            # # decode sequence if queue has 4 color 
            # if len(queue) == 4:
            #    print(decode_sequence(queue))
            #    queue.clear()

            # Code to check patterns
            
            

        if 'video_file' in kwargs:
            # forward by milliseconds
            milliseconds += MIN_COLOR_DURATION
            vid.set(cv2.CAP_PROP_POS_MSEC, milliseconds)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    vid.release()
    cv2.destroyAllWindows()
    return color_seq

print(capture_color_sequence())
# seq = capture_color_sequence()
# print(len(seq))