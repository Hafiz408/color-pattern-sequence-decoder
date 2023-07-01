# importing required libraries
import cv2
import numpy as np
import time
from env import *
import collections

def skip_frames(fps,duration):
    return round(duration/(1000/fps))

SKIP_FR = skip_frames(FPS,MIN_COLOR_DURATION)

# map color pixel values to closest valid pixel values
def closest_valid_value(input_value):
  dec_codes = np.array(VALID_DEC_CODES)
  min = (np.abs(dec_codes - input_value)).min()
  if min <= THRESHOLD:
    i = (np.abs(dec_codes - input_value)).argmin()
    return dec_codes[i]
  else:
    return -1

def closest_rgb(r,g,b):
   r_valid = closest_valid_value(r)
   g_valid = closest_valid_value(g)
   b_valid = closest_valid_value(b)

   return (r_valid, g_valid, b_valid)

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
    partial_buffer=collections.deque()
    full_buffer = collections.deque()

    color_seq = []

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

        # For final pattern after break
        if not valid:
            if right==4:
                tup=tuple(full_buffer)
                if tup in keys:
                    if len(partial_buffer)>1 and len(partial_buffer)<=3:
                        partialMatch(tuple(partial_buffer))
                    partial_buffer.clear()
                    print("Valid Pattern ",valid_pattern[tup])
                    full_buffer.clear()
                else:
                    if len(partial_buffer)>1 and len(partial_buffer)<=3:
                        partialMatch(tuple(partial_buffer))
                        temp=len(partial_buffer)
                        partial_buffer.clear()
                    else:
                        print("Invalid Pattern")
                        temp=1
                    partial_buffer.append(full_buffer[0])
                    while temp:
                        full_buffer.popleft()
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
            b_estimate = int(np.mean(b))
            g_estimate = int(np.mean(g))
            r_estimate = int(np.mean(r))

        # finding closest rgb from estimate
        rgb = closest_rgb(r_estimate, g_estimate, b_estimate)
        color = dec_to_color.get(rgb, '404')

        # print((r_estimate,g_estimate,b_estimate), rgb, color)

        color_seq.append(color)

        # Pattern matchining
        if right==4:
                tup=tuple(full_buffer)
                if tup in keys:
                    if len(partial_buffer)>1 and len(partial_buffer)<=3:
                        partialMatch(tuple(partial_buffer))
                    partial_buffer.clear()
                    print("Valid Pattern ",valid_pattern[tup])
                    full_buffer.clear()
                    right=0
                else:
                    if len(partial_buffer)>1 and len(partial_buffer)<=3:
                        partialMatch(tuple(partial_buffer))
                        temp=len(partial_buffer)
                        partial_buffer.clear()
                    else:
                        print("Invalid Pattern")
                        temp=1
                    partial_buffer.append(full_buffer[0])
                    while temp:
                        full_buffer.popleft()
                        right-=1
                        temp-=1

        if color != '404':
            if right>2 and (full_buffer[right-1]==color  and full_buffer[right-2]==color):
                continue
            full_buffer.append(color)
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

print(capture_color_sequence(video_file='shortVideo.mp4'))
# seq = capture_color_sequence()
# print(len(seq))
# print(seq)